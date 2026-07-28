from django.shortcuts import render, redirect, get_object_or_404
import json
import uuid
from django.contrib import messages
from core.models import Product, Order, OrderItem, Transaction


def cart(request):
    cart_session = request.session.get('cart', {})
    cart_items = []
    subtotal = 0.0

    for product_id, quantity in cart_session.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = float(product.price) * quantity
            subtotal += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
        except Product.DoesNotExist:
            continue

    shipping_cost = 15.00 if cart_items else 0.00
    grand_total = subtotal + shipping_cost

    context = {
        'page_title': 'Cart',
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
        'cart_count': sum(cart_session.values()),
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_session = request.session.get('cart', {})
    
    # Convert product_id to string since session keys are strings in JSON
    pid_str = str(product_id)
    
    try:
        quantity = int(request.GET.get('quantity', request.POST.get('quantity', 1)))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1
    
    # Increment quantity
    cart_session[pid_str] = cart_session.get(pid_str, 0) + quantity
    
    request.session['cart'] = cart_session
    messages.success(request, f"Added {quantity} x '{product.name}' to your cart.")
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart_session = request.session.get('cart', {})
    pid_str = str(product_id)
    
    if pid_str in cart_session:
        del cart_session[pid_str]
        request.session['cart'] = cart_session
        
    return redirect('cart')


def remove_one_from_cart(request, product_id):
    cart_session = request.session.get('cart', {})
    pid_str = str(product_id)
    
    if pid_str in cart_session:
        if cart_session[pid_str] > 1:
            cart_session[pid_str] -= 1
        else:
            del cart_session[pid_str]
        request.session['cart'] = cart_session
        
    return redirect('cart')


def update_cart(request, product_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        cart_session = request.session.get('cart', {})
        pid_str = str(product_id)
        
        if pid_str in cart_session:
            if quantity > 0:
                cart_session[pid_str] = quantity
            else:
                del cart_session[pid_str]
            request.session['cart'] = cart_session
            
    return redirect('cart')


from django.contrib.auth.decorators import login_required
from core.models import Order, OrderItem

from .forms import CheckoutForm

@login_required
def checkout(request):
    cart_session = request.session.get('cart', {})
    if not cart_session:
        return redirect('cart')

    cart_items = []
    subtotal = 0.0

    for product_id, quantity in cart_session.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = float(product.price) * quantity
            subtotal += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
        except Product.DoesNotExist:
            continue

    shipping_cost = 15.00 if cart_items else 0.00
    grand_total = subtotal + shipping_cost

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Generate unique order code
            order_code = str(uuid.uuid4()).replace('-', '')[:12]
            
            # Create order in database
            order = Order.objects.create(
                user=request.user,
                total_price=grand_total,
                status='pending',
                order_code=order_code
            )
            
            # Create OrderItem records
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )
                
            # Trigger M-Pesa STK Push immediately!
            from .utils import initiate_stk_push
            phone = form.cleaned_data.get('mobile')
            response, _ = initiate_stk_push(
                phone=phone,
                amount=grand_total,
                order_reference=order_code
            )
            
            if response and response.get('ResponseCode') == '0':
                # Update order with merchant_request_id
                merchant_request_id = response.get('MerchantRequestID')
                order.merchant_request_id = merchant_request_id
                order.save()
                
                Transaction.objects.create(
                    user=request.user,
                    order=order,
                    amount=grand_total,
                    phone_number=phone,
                    checkout_request_id=response.get('CheckoutRequestID', ''),
                    status='pending',
                    response_code=response.get('ResponseCode'),
                    response_description=response.get('ResponseDescription')
                )
                messages.success(request, 'Order placed. M-Pesa STK Push sent successfully!')
            else:
                err_desc = response.get('ResponseDescription', 'STK Push failed.') if response else 'STK Push failed.'
                messages.warning(request, f"Order placed, but payment prompt failed: {err_desc}")

            # Empty user's shopping cart session
            request.session['cart'] = {}
            
            return redirect('my_orders')
    else:
        form = CheckoutForm()

    context = {
        'page_title': 'Checkout',
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
        'form': form,
    }
    return render(request, 'checkout.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .utils import get_access_token

@ensure_csrf_cookie
def get_access_token_view(request):
    access_token, expires_in = get_access_token()

    if access_token:
        return JsonResponse({
            'access_token': access_token,
            'expires_in': expires_in
        })
    else:
        return JsonResponse({'error': 'Failed to generate access token'}, status=500)


from django.contrib.auth.decorators import login_required

@login_required
def initiate_payment_page(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    context = {
        'order': order,
        'page_title': f'Pay Order #{order.id}',
    }
    return render(request, 'accounts/payment.html', context)


@login_required
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        if not phone:
            messages.error(request, 'Please provide a valid M-Pesa phone number.')
            return redirect('initiate_payment_page', order_id=order.id)
            
        from .utils import initiate_stk_push
        response, _ = initiate_stk_push(
            phone=phone,
            amount=order.total_price,
            order_reference=order.order_code
        )
        
        if response and response.get('ResponseCode') == '0':
            merchant_request_id = response.get('MerchantRequestID')
            order.merchant_request_id = merchant_request_id
            order.save()
            
            Transaction.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price,
                phone_number=phone,
                checkout_request_id=response.get('CheckoutRequestID', ''),
                status='pending',
                response_code=response.get('ResponseCode'),
                response_description=response.get('ResponseDescription')
            )
            messages.success(request, 'STK Push sent successfully. Please check your phone.')
        else:
            err_desc = response.get('ResponseDescription', 'Payment initiation failed.') if response else 'Payment initiation failed.'
            messages.error(request, err_desc)
            
    return redirect('my_orders')


import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            # Parse the callback data
            callback_data = json.loads(request.body)
            logger.info(f"M-Pesa Callback received: {callback_data}")
            
            stk_callback = callback_data['Body']['stkCallback']

            merchant_request_id = stk_callback.get('MerchantRequestID')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')

            transaction = Transaction.objects.filter(checkout_request_id=checkout_request_id).first()
            if not transaction:
                logger.error(f"Transaction not found for CheckoutRequestID: {checkout_request_id}")
                return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Transaction not found'})
            order = transaction.order

            # Extract metadata if payment was successful
            if result_code == 0:
                metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                
                amount = 0
                receipt_id = ''
                phone_number = ''
                
                # Metadata items can be list of dicts: [{'Name': 'Amount', 'Value': 1000}, ...]
                for item in metadata:
                    name = item.get('Name')
                    val = item.get('Value')
                    if name == 'Amount':
                        amount = val
                    elif name == 'MpesaReceiptNumber':
                        receipt_id = val
                    elif name == 'PhoneNumber':
                        phone_number = val

                # Update transaction
                transaction.amount = amount
                transaction.transaction_id = receipt_id
                transaction.phone_number = phone_number
                transaction.status = 'success'
                transaction.response_code = str(result_code)
                transaction.response_description = result_desc
                transaction.save()

                # Update order
                order.status = 'paid'
                order.receipt_number = receipt_id
                order.save()
                logger.info(f"Payment successful for Order #{order.id}. Receipt: {receipt_id}")

            else:
                # Failed transaction
                transaction.status = 'failed'
                transaction.response_code = str(result_code)
                transaction.response_description = result_desc
                transaction.save()
                logger.warning(f"Payment failed for Order #{order.id}. Code: {result_code}, Desc: {result_desc}")

            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Success'})

        except Exception as e:
            logger.error(f"Callback error processing payload: {e}")
            return JsonResponse({'ResultCode': 1, 'ResultDesc': str(e)})

    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid request method'})



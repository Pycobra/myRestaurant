from rest_framework import serializers
from apps.checkout.models import DeliveryOptions, PaymentSelections
from apps.order.models import OrderReciept, OrderedItemDetail, Checkout
from apps.product.models import Product



class DeliveryOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= DeliveryOptions
        fields="__all__"
                

class PaymentSelectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= PaymentSelections
        fields=("id", 'name', 'default')

    
class OrderRecieptSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReciept
        fields = ('user', 'total_quantity', 'delivery_address', 
        'delivery_instructions', 'total_paid', 'payment_option')
        
    def create(self, validated_data):
        ref =self.initial_data.get('ref')
        payment_name =self.initial_data.get('payment_name') 
        amount= self.initial_data.get('amount'),
        instance = self.Meta.model.objects.create(
            user= self.validated_data.get('user'), 
            total_quantity= self.validated_data.get('total_quantity'), 
            delivery_address= self.validated_data.get('delivery_address'), 
            delivery_instructions= self.validated_data.get('delivery_instructions'), 
            total_paid= self.validated_data.get('total_paid'), 
            payment_option= self.validated_data.get('payment_option'),
        )
        for item in self.initial_data.get('cartItems'):
            OrderedItemDetail.objects.create(
                order=instance, product=Product.objects.get(id=item['id']), 
                amount=item['total_price'], quantity=item['quantity']
                #special_instruction: item['instruction'], 
                #ingredient: item['ingredientList']
            )
        print(amount, amount[0], ref, payment_name, '\\\\\\====')
        verified = instance.verify_payment(amount[0], ref, payment_name)
        if verified:
            instance.verified = True
            instance.save()
            CheckoutSerializer(data={'order':instance.id, 'ref':ref})
        else:
            raise serializers.ValidationError("Your payment verification failed")
        return instance



class OrderedItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItemDetail
        fields = ('order', 'product', 'amount', 'quantity')


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('order', 'ref')

class PaymentVerificationDataSerializer(serializers.Serializer):
    ref = serializers.CharField()
    payment_name = serializers.CharField()


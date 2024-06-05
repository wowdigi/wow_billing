from rest_framework import serializers
from .models import *
from datetime import datetime


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'

class BillingDetailSerializer(serializers.ModelSerializer):
     id = serializers.IntegerField(required=False)

     class Meta:
         model = BillingDetail
         exclude=('mst_ref_id',)

class BillingMstSerializer(serializers.ModelSerializer):
    items = BillingDetailSerializer(many=True)

    class Meta:
        model = BillingMst
        fields = '__all__'

    def create(self , validated_data):
        details_data = validated_data.pop('items')
        # validated_data['recharge_wallet'] = sum(Decimal(item["amount"]) for item in wallet_detail)
        ordermst = BillingMst.objects.create(**validated_data)
        for detail_data in details_data:
            # detail_data['created_by'] = validated_data['created_by']
            BillingDetail.objects.create(mst_ref_id=ordermst, **detail_data)
        return ordermst

    def update(self ,instance, validated_data):
        details_data = validated_data.pop('items')
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # instance.recharge_wallet = sum(Decimal(item["amount"]) for item in wallet_detail)
        instance.save()

        for child_data in details_data:
            child_id = child_data.get('id')
            if child_id:
                child = BillingDetail.objects.get(id=child_id, mst_ref_id=instance)
                # child.modified_by = validated_data['modified_by']
                for key, value in child_data.items():
                    setattr(child, key, value)
                child.save()
            else:
                # child_data['created_by'] = validated_data['modified_by']
                BillingDetail.objects.create(mst_ref_id=instance, **child_data)

        return instance
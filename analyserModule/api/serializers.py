from rest_framework import serializers
# class BankDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankDetails
#         fields = ['id', 'bankName']


class GrossSummarySerializer(serializers.Serializer):

    avgBalance = serializers.DecimalField(max_digits=None, decimal_places=None)


class ParticularBankSerializer(serializers.Serializer):
    bankName = serializers.CharField(max_length=100)


class BankAnalyserSerializer(serializers.Serializer):
    volatilityScore = serializers.IntegerField()
    bankName = serializers.CharField(max_length=100)
    avgMonthlySpending = serializers.DecimalField(
        max_digits=None, decimal_places=None)
    percentMonthlySpending = serializers.DecimalField(
        max_digits=None, decimal_places=None)
    SourcesOfLargeCredit = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    SourcesOfLargeDebit = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    frequencyOfCreditPayments = serializers.IntegerField()
    frequencyOfDebitPayments = serializers.IntegerField()
    frequencyOfPayment = serializers.IntegerField()
    spendingToIncomeRatio = serializers.DecimalField(
        max_digits=None, decimal_places=None)
    daysToSpend50Percent = serializers.IntegerField()
    daysToSpend80Percent = serializers.IntegerField()
    recurringPayment = serializers.IntegerField()


#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return BankDetails.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.bankName = validated_data.get('bankName', instance.bankName)
#         instance.startDate = validated_data.get(
#             'validated_data', instance.startDate)
#         instance.endDate = validated_data.get(
#             'validated_data', instance.endDate)
#         instance.addedAccount = validated_data.get(
#             'validated_data', instance.addedAccount)
#         instance.save()
#         return instance

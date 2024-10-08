from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Feature
from .serializers import FeatureSerializer

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

class FeatureView(APIView):
    def get(self, request):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeatureSerializer(data=request.data)
        if serializer.is_valid():
            feature_data = serializer.validated_data
         
            input_data = pd.DataFrame({
                'ProviderId': [feature_data['ProviderId']],
                'ProductId': [feature_data['ProductId']],
                'ChannelId': [feature_data['ChannelId']],
                'Amount': [feature_data['Amount']],
                'Transaction_Hour': [feature_data['Transaction_Hour']],
                'Transaction_Day': [feature_data['Transaction_Day']],
                'Average_transaction_amount': [feature_data['Average_transaction_amount']],
                'STD_Transaction_Amount': [feature_data['STD_Transaction_Amount']],
                'Transaction_Month': [feature_data['Transaction_Month']],
                'ProductCategory_airtime': [feature_data['ProductCategory'] == 'airtime'],
                'ProductCategory_data_bundles': [feature_data['ProductCategory'] == 'data_bundles'],
                'ProductCategory_financial_services': [feature_data['ProductCategory'] == 'financial_services'],
                'ProductCategory_movies': [feature_data['ProductCategory'] == 'movies'],
                'ProductCategory_other': [feature_data['ProductCategory'] == 'other'],
                'ProductCategory_ticket': [feature_data['ProductCategory'] == 'ticket'],
                'ProductCategory_transport': [feature_data['ProductCategory'] == 'transport'],
                'ProductCategory_tv': [feature_data['ProductCategory'] == 'tv'],
                'ProductCategory_utility_bill': [feature_data['ProductCategory'] == 'utility_bill']
            })

            continuous_features = ['Amount', 'Transaction_Hour', 'Transaction_Day', 
                                    'Average_transaction_amount', 'STD_Transaction_Amount', 'Transaction_Month']


            scaler = StandardScaler()
            input_data[continuous_features] = scaler.fit_transform(input_data[continuous_features])
            
            model = joblib.load('C:/Users/user/Documents/Programming/Kifiya_10X/Credit_Risk_Model/Models/GradientBoostingClassifier_model.pkl') 
            prediction = model.predict(input_data)
            if prediction == 0:
                response = 'No Risk'
            else:
                response = 'Has Risk'
            return Response({'prediction': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
# модель для сбора данных для рекомендаций

#from django.db import models
#from django.contrib.auth.models import User
#
#class UserActivity(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    product = models.ForeignKey(Product, on_delete=models.CASCADE)
#    action = models.CharField(max_length=50)  # e.g. 'viewed', 'purchased', 'liked'
#    timestamp = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return f"{self.user.username} {self.action} {self.product.name}"





# рекомендации


#import pandas as pd
#from sklearn.metrics.pairwise import cosine_similarity
#
## Получаем данные из базы
#user_activity = UserActivity.objects.all()
#data = {
#    'user_id': [],
#    'product_id': [],
#    'action': []
#}
#
#for activity in user_activity:
#    data['user_id'].append(activity.user.id)
#    data['product_id'].append(activity.product.id)
#    data['action'].append(activity.action)
#
#df = pd.DataFrame(data)
#

#user_product_matrix = df.pivot_table(index='user_id', columns='product_id', values='action', fill_value=0)
#

#cosine_sim = cosine_similarity(user_product_matrix)
#

#cosine_sim_df = pd.DataFrame(cosine_sim, index=user_product_matrix.index, columns=user_product_matrix.index)
#
#def get_recommendations(user_id, cosine_sim_df, top_n=5):
#    # Получаем схожесть текущего пользователя с другими пользователями
#    similar_users = cosine_sim_df[user_id].sort_values(ascending=False)
#    
#    # Получаем продукты, которые покупали схожие пользователи
#    recommended_products = []
#
#    for other_user in similar_users.index:
#        if other_user == user_id:
#            continue
#        # Получаем продукты, купленные другим пользователем
#        purchased_products = df[df['user_id'] == other_user]['product_id'].values
#        recommended_products.extend(purchased_products)
#        
#        if len(recommended_products) >= top_n:
#            break
#
#    return list(set(recommended_products))[:top_n]
#
#recommended = get_recommendations(user_id=1, cosine_sim_df=cosine_sim_df)
#print(recommended)  





#контролер для рекомендаций


#from rest_framework import viewsets
#from rest_framework.response import Response
#from .models import Product
#from .serializers import ProductSerializer
#
#class RecommendationViewSet(viewsets.ViewSet):
#    def list(self, request, user_id):
#        recommended_product_ids = get_recommendations(user_id, cosine_sim_df)
#        recommended_products = Product.objects.filter(id__in=recommended_product_ids)
#        serializer = ProductSerializer(recommended_products, many=True)
#        return Response(serializer.data)

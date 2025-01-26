from django.shortcuts import get_object_or_404
from django.contrib.auth import login ,logout,authenticate

from rest_framework import generics,views,serializers,status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from .models import ProductModel,CategoryModel,OrderItemModel,OrderModel,CartModel,ProfileModel
from .serializers import ProductSerializer,CategorySerializer,OrderItemSerializer,OrderSerializer,CartSerializer,ProfileSerialzer
from .permissions import IsStaffPermission

class RegisterView(generics.CreateAPIView):

    queryset=ProfileModel.objects.all()
    serializer_class=ProfileSerialzer
    
RegisterViewClass=RegisterView.as_view()

class LoginView(views.APIView):

    permission_classes=[]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."},status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                token = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User account is inactive."},status=status.HTTP_403_FORBIDDEN,)
        else:
            return Response({"error": "Invalid username or password."},status=status.HTTP_401_UNAUTHORIZED,)
        
LoginViewClass=LoginView.as_view()

class LogoutView(views.APIView):

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)

LogoutViewClass=LogoutView.as_view()

class ProductListCreateView(generics.ListCreateAPIView):

    queryset=ProductModel.objects.all().exclude(Inventory=0)
    serializer_class=ProductSerializer
    permission_classes=[IsStaffPermission]

    def perform_create(self, serializer):
        Description=serializer.validated_data.get("Description")
        if Description is None:
            Description=serializer.validated_data.get("Name")
        serializer.save(Description=Description)

ProductListCreateViewClass=ProductListCreateView.as_view()

class ProductDetailView(generics.RetrieveAPIView):
    queryset=ProductModel.objects.all().exclude(Inventory=0)
    serializer_class=ProductSerializer
    lookup_field='pk'

    def get(self, request, *args, **kwargs):
        if self.queryset is not None: 
            return super().get(request, *args, **kwargs)
        return Response({"No-Item":"The item you are looking is out of stock","Visit Later":"Soon the product will be avialable come back soon"},status=status.HTTP_404_NOT_FOUND)

ProductDetailViewClass=ProductDetailView.as_view()

class ProductUpdateView(generics.UpdateAPIView):
    queryset=ProductModel.objects.all().exclude(Inventory=0)
    serializer_class=ProductSerializer
    lookup='pk'
    permission_classes=[IsStaffPermission]
    
    def get(self,request,pk=None,*args,**kwargs):
        instance=get_object_or_404(ProductModel,pk=pk)
        serializer=ProductSerializer(instance,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        Description=serializer.validated_data.get("Description")
        if Description is None:
            Description=serializer.validated_data.get("Name")
        serializer.save(Description=Description)

ProductUpdateViewClass=ProductUpdateView.as_view()

class ProductDeleteView(generics.DestroyAPIView):
    queryset=ProductModel.objects.all().exclude(Inventory=0)
    serializer_class=ProductSerializer
    lookup='pk'
    permission_classes=[IsStaffPermission]

    def get(self,request,pk=None):
        if pk is not None:
            queryset=get_object_or_404(ProductModel,pk=pk)
            serialize=ProductSerializer(queryset,context={"request":request})
            return Response(serialize.data,status=status.HTTP_200_OK)
        else:
            return Response({"pk":"pk is not given! please provide it to delete the product"},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.delete()
        serialzer=ProductSerializer(instance,context={"request":request})
        return Response(serialzer.data,status=status.HTTP_204_NO_CONTENT)

ProductDeleteViewClass=ProductDeleteView.as_view()

class CategoryListCreatView(generics.ListCreateAPIView):
    queryset=CategoryModel.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsStaffPermission]

CategoryListCreatViewClass=CategoryListCreatView.as_view()

class CategoryDetailView(generics.RetrieveAPIView):
    queryset=CategoryModel.objects.all()
    serializer_class=CategorySerializer

    def get(self,request,pk=None):
        Result={}
        Category=get_object_or_404(CategoryModel,pk=pk)
        Result["id"]=Category.pk
        #Category=Category.Name
        Result["Category"]=Category.Name
        product_query=ProductModel.objects.filter(Category=Category)[:5]
        serialzer=ProductSerializer(product_query,context={'request':request},many=True)
        Result["Products"]=serialzer.data
        return Response(Result,status=status.HTTP_200_OK)

CategoryDetailViewClass=CategoryDetailView.as_view()

class CategoryDeleteView(generics.DestroyAPIView):
    queryset=CategoryModel.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsStaffPermission]

    def get(self,requset,pk=None):
        if pk is not None:
            instance=get_object_or_404(CategoryModel,pk=pk)
            serialize=CategorySerializer(instance)
            return Response(serialize.data,status=status.HTTP_200_OK)
        else:
            return Response({"pk is not given":"Provide it to delete the category"},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.delete()
        serialzer=CategorySerializer(instance)
        return Response(serialzer.data,status=status.HTTP_204_NO_CONTENT)

CategoryDeleteViewClass=CategoryDeleteView.as_view()

class ListCreateOrderView(generics.ListCreateAPIView):
    #Returning the product as catgeory-delevered,cancelled,proccess
    queryset=OrderItemModel.objects.all()
    serializer_class=OrderItemSerializer
    lookup='pk'

    def get(self, request, *args, **kwargs):
        user=self.request.user
        if user is None or user.is_anonymous:
            raise ValidationError("Login is required for view the list of order")
        Result={}
        Order_qs=OrderModel.objects.filter(User=user).filter(Status="Pending")
        process=[]
        for i in Order_qs:
            Product=(OrderItemModel.objects.filter(Order=i))
            process.append(OrderItemSerializer(Product,many=True,context={'request':request}).data)
        Result['Pending']=process
        Shipped=[]
        ship_qs=OrderModel.objects.filter(User=user).filter(Status="Shipped")
        for i in ship_qs:
            product=OrderItemModel.objects.filter(Order=i)
            Shipped.append(OrderItemSerializer(product,many=True,context={'request':request}).data)
        Result['Shipped']=Shipped
        Others=[]
        Other_qs=OrderModel.objects.filter(User=user).exclude(Status="Pending").exclude(Status="Shipped")
        for i in Other_qs:
            product=OrderItemModel.objects.filter(Order=i)
            Others.append(OrderItemSerializer(product,many=True,context={'request':request}).data)
        Result["Other"]=Others
       
        return Response(Result,status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        quantity=serializer.validated_data.get("Quantity")
        Product=serializer.validated_data.get("Product")
        Product_quantity=Product.Inventory
        if(Product_quantity>=quantity):
            Product.Inventory=Product_quantity-quantity
            Product.save()
            serializer.save()
           
        else:
            if(Product_quantity<=1):
                msg="Only "+str(Product_quantity)+" product is available!"
            else:
                msg="Only "+str(Product_quantity)+" products is available!"
            raise serializers.ValidationError(msg)
    

ListOrderViewClass=ListCreateOrderView.as_view()

class OrderDetailView(generics.RetrieveAPIView):
    queryset=OrderItemModel.objects.all()
    serializer_class=OrderItemSerializer

    def get(self, request,pk=None, *args, **kwargs):
        queryset=get_object_or_404(OrderItemModel,pk=pk)
        serializer=OrderItemSerializer(queryset,context={'request':request})
        Result=serializer.data
        Result['Order Date']=queryset.Order.OrderDate
        Result['Order Status']=queryset.Order.Status
        return Response(Result,status=status.HTTP_200_OK)

OrderDetailViewClass=OrderDetailView.as_view()

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset=OrderModel.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsStaffPermission]

    def get(self,request,pk=None):
        user=self.request.user
        if user is None or user.is_anonymous:
            raise ValidationError("Login is required for view the list of order")
        if pk is None:
            raise ValidationError("Please provide the Pk to update")
        
        qs=OrderItemModel.objects.filter(Order__pk=pk)
        serializer=OrderItemSerializer(qs,context={'request':request},many=True).data
        return Response(serializer,status=status.HTTP_200_OK)

OrderStatusUpdateViewClass=OrderStatusUpdateView.as_view()

class searchView(generics.ListAPIView):
    queryset=ProductModel.objects.all()
    serializer_class=ProductSerializer

    def get(self, request, *args, **kwargs):
        key=self.request.GET.get("key")
        Result={}
        qs1=ProductModel.objects.exclude(Inventory=0).filter(Name__contains=key)
        qs2=ProductModel.objects.exclude(Inventory=0).filter(Description__contains=key)
        qs=(qs1 | qs2).distinct()
        serialize_product=ProductSerializer(qs,many=True,context={'request':request})
        Result['products']=serialize_product.data
        qs3=CategoryModel.objects.filter(Name__contains=key)
        serialize_category=CategorySerializer(qs3,many=True)
        Result["category"]=serialize_category.data
        if(Result['products']==[] and Result["category"]==[] ):
            return Response({
                "Not found":"The product or category you are looking for not available",
                "check":"Check whether you speel correctly"
                },status=status.HTTP_404_NOT_FOUND)
        return Response(Result,status=status.HTTP_200_OK)

searchViewClass=searchView.as_view()

class CartAddListView(generics.ListCreateAPIView):
    queryset=CartModel.objects.all()
    serializer_class=CartSerializer

    def get(self, request, *args, **kwargs):
        user=self.request.user
        if user is None or user.is_anonymous:
            raise ValidationError({'Login':"You must login to add or view the element in the cart"})
        queryset=CartModel.objects.filter(User=user)
        serializer=CartSerializer(queryset,many=True)
        if(serializer.data==[]):
            return Response({"Empty":"Your cart is empty add the products to it"},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(User=user)

CartAddListViewClass=CartAddListView.as_view()

class CartDetailView(generics.RetrieveAPIView):
    queryset=CartModel.objects.all()
    serializer_class=CartSerializer

    def get(self, request,pk=None, *args, **kwargs):
        user=self.request.user
        if user is None or user.is_anonymous:
            raise ValidationError({"Login":"Login to view the cart"})
        query=CartModel.objects.filter(User=user)
        product=get_object_or_404(query,pk=pk)
        serialize=CartSerializer(product)
        product_serilize=ProductSerializer(product.Product,context={"request":request})
        price=product_serilize.data['Price']
        serialize=serialize.data
        quantity=serialize['Quantity']
        serialize['Price']=price*quantity
        return Response(serialize,status=status.HTTP_200_OK)

CartDetailViewclass=CartDetailView.as_view()

class CartRemoveView(generics.DestroyAPIView):
    queryset=CartModel.objects.all()
    serializer_class=CartSerializer

    def get(self,request,pk=None):
        user=self.request.user
        if user is None or user.is_anonymous:
            raise ValidationError({"Login":"Login to view the cart"})
        product=get_object_or_404(CartModel,pk=pk)
        serialize=CartSerializer(product)
        return Response(serialize.data,status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        user=self.request.user
        if user is None or user.is_anonymous:
            raise ValidationError({"Login":"Login to view the cart"})
        self.queryset=CartModel.objects.filter(User=user)
        return super().destroy(request, *args, **kwargs)

CartRemoveViewClass=CartRemoveView.as_view()

class PageNotFoundView(views.APIView):
    def get(self, request, format=None):
        return Response({"Not Found":"The URL you are searching is not avliable.Check the URL"},status=status.HTTP_404_NOT_FOUND)
    
PageNotFoundViewClass=PageNotFoundView.as_view()

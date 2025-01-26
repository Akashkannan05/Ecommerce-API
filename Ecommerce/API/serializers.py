from rest_framework import serializers
from .models import ProductModel,OrderItemModel,OrderModel,CategoryModel,CartModel,ProfileModel
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=CategoryModel
        fields=[
            'id',
            'Name',
        ]

class ProductSerializer(serializers.ModelSerializer):
    URL=serializers.HyperlinkedIdentityField(
        view_name="Detail of the product",
        lookup_field='pk',
    )
    class Meta:
        model=ProductModel
        fields=[
            "id",
            "URL",
            "Name",
            "Description",
            "Price",
            "In_Dollars",
            "Image",
            "Category",
            "Inventory",
        ]
    def validate_Price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_Inventory(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory cannot be negative.")
        return value
    
class OrderSerializer(serializers.ModelSerializer):
       
    User=serializers.CharField(read_only=True)
    class Meta:
        model=OrderModel
        fields=[
            'id',
            'User',
            'OrderDate',
            'Status'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    
    Status=serializers.CharField(read_only=True)
    Order=serializers.CharField(read_only=True)
    class Meta:
        model=OrderItemModel
        fields=[
            'id',
            'Order',
            'Product',
            'Quantity',
            #Property
            'Price',
            'TotalPrice',
            'Status'
        ]

    def create(self, validated_data):
        User=self.context['request'].user
        if User is None :
            raise ValidationError("Login to order the item")
        Status="Pending"
        UserOrder=OrderModel(User=User,Status=Status)
        UserOrder.save()
        validated_data['Order']=UserOrder
        return super().create(validated_data)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartModel
        fields=[
            'id', 
            'Product',
            'Quantity',
            'Date'
        ]

class ProfileSerialzer(serializers.ModelSerializer):
    UserName=serializers.CharField(write_only=True)
    Password=serializers.CharField(write_only=True)
    Verify_Password=serializers.CharField(write_only=True)
    Email=serializers.EmailField(write_only=True)
    class Meta:
        model=ProfileModel
        fields=[
            'id',
            'UserName',
            'Password',
            'Verify_Password',
            'Email',
            'PhoneNumber',
            'Address',
            'DateOfBirth',
            'ProfilePic',
        ]
    
    def validate_PhoneNumber(self, value):
        length=len(value)
        if value[1:].isnumeric():
            if length==13 and value[0]=='+':
                return value
            elif length>=10:
                raise serializers.ValidationError("Country code is missing")
            else:
                raise serializers.ValidationError("Enter the valid phone number")
        else:
            raise serializers.ValidationError("Enter only digits No other charcters are allowed than + and digit")
    def validate(self,data):
        if data['Password']==data['Verify_Password']:
            return data
        raise serializers.ValidationError({"Password doesn't match":"The value given in password and varify password field are not same! Check the password!"})
    
    def create(self, validated_data):
        UserName=validated_data.pop("UserName")
        UserCheck= User.objects.filter(username=UserName)
        if UserCheck.exists():
            raise ValidationError("The Username already exisit Try any other username")
        Password=validated_data.pop("Password")
        Email=validated_data.pop("Email")
        validated_data.pop("Verify_Password")
        AddUser=User(username=UserName,email=Email)
        AddUser.set_password(Password)
 
        AddUser.save()
        #USER=get_object_or_404(User,username=UserName)
        validated_data['User']=AddUser
  
        return super().create(validated_data)

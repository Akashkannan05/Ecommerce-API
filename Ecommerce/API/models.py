from django.db import models
from django.conf import settings

User=settings.AUTH_USER_MODEL

class CategoryModel(models.Model):
    Name=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.Name}"

class ProductModel(models.Model):
    Name=models.CharField(max_length=30)
    Description=models.TextField(null=True)
    Price=models.DecimalField(max_digits=5,decimal_places=3)
    Image=models.ImageField(blank=True,null=True,upload_to="images")
    Category=models.ForeignKey(CategoryModel,on_delete=models.SET_NULL,null=True)
    Inventory=models.IntegerField()

    def __str__(self):
        if(self.Inventory!=0):
            return f"{self.pk}){self.Name}-{self.Price}"
        else:
            return f"{self.Name}-OutOfStock"
    
    @property
    def In_Dollars(self):
        return "%.2f"%(float(self.Price/81))

Choice=(
    ("Pending","Pending"),
    ("Processing","Processing"),
    ("Shipped","Shipped"),
    ("Delivery","Delivery"),
    ("Cancelled","Cancelled")

)

class OrderModel(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    OrderDate=models.DateTimeField(auto_created=True,auto_now=True)
    Status=models.CharField(choices=Choice,default="Pending",max_length=20)

    def __str__(self):
        return f"{self.pk}){self.User}-{self.Status}"
    


class OrderItemModel(models.Model):

    Order=models.ForeignKey(OrderModel,on_delete=models.SET_NULL,null=True)
    Product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    Quantity=models.IntegerField()


    def __str__(self):
        return f"{self.Product.Name}-{self.Quantity}-INR{self.TotalPrice}"
    
    @property
    def Price(self):
        return float(self.Product.Price)
    
    @property
    def TotalPrice(self):
        return float(self.Quantity*self.Price)

class CartModel(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    Product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    Date=models.DateTimeField(auto_created=True,auto_now=True)
    Quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.Product}"
    
class ProfileModel(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE)
    PhoneNumber=models.CharField(max_length=13)
    Address=models.TextField(null=True)
    DateOfBirth=models.DateField(null=True)
    ProfilePic=models.ImageField(blank=True,null=True,upload_to="images/profile")

    def __str__(self):
        return f"{self.PhoneNumber}"

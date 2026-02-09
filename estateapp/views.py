from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .models import Property, Register, ContactMessage,Enquiry
from .serializers import PropertySerializer, RegisterSerializer, ContactSerializer,EnquirySerializer


def home(request):
    return HttpResponse("Welcome to Estate API!")

@api_view(['POST'])
def register(request):
    data = request.data
    if Register.objects.filter(email=data.get('email')).exists():
        return Response({'error': 'Email already exists'}, status=400)

    Register.objects.create(
        fname=data.get('fname'),
        mobile=data.get('mobile'),
        email=data.get('email'),
        password=make_password(data.get('password'))
    )

    return Response({'message': 'Registration successful'}, status=201)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = Register.objects.get(email=email)
    except Register.DoesNotExist:
        return Response({'error': 'Invalid email'}, status=400)

    if check_password(password, user.password):
        return Response({
            'id': user.id,
            'fname': user.fname,
            'email': user.email,
            'mobile': user.mobile
        })

    return Response({'error': 'Invalid password'}, status=400)


@api_view(['GET', 'POST'])
def property_list(request):
    if request.method == 'GET':
        properties = Property.objects.all().order_by('-id')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'DELETE'])
def property_detail(request, pk):
    try:
        prop = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({'error': 'Property not found'}, status=404)

    if request.method == 'GET':
        return Response(PropertySerializer(prop).data)

    if request.method == 'PATCH':
        serializer = PropertySerializer(prop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    prop.delete()
    return Response({'message': 'Property deleted'})

@api_view(['GET', 'POST'])
def contact_message(request):

    if request.method == 'GET':
        messages = ContactMessage.objects.all().order_by('-id')
        serializer = ContactSerializer(messages, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact message sent successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def enquiry(request):
    if request.method == 'GET':
        enquiries = Enquiry.objects.all().order_by('-id')
        serializer = EnquirySerializer(enquiries, many=True)
        return Response(serializer.data)

    # POST
    serializer = EnquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Enquiry sent successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cart_list(request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_items = Cart.objects.filter(user_id=user_id)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_cart(request):
    user_id = request.data.get("user_id")
    property_id = request.data.get("property_id")

    if not user_id or not property_id:
        return Response(
            {"error": "user_id and property_id required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = Register.objects.get(id=user_id)
        property_obj = Property.objects.get(id=property_id)
    except (Register.DoesNotExist, Property.DoesNotExist):
        return Response(
            {"error": "User or Property not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        property=property_obj
    )

    if not created:
        return Response(
            {"message": "Already in cart"},
            status=status.HTTP_200_OK
        )

    serializer = CartSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def remove_from_cart(request, pk):
    try:
        cart_item = Cart.objects.get(pk=pk)
        cart_item.delete()
        return Response(
            {"message": "Removed from cart"},
            status=status.HTTP_204_NO_CONTENT
        )
    except Cart.DoesNotExist:
        return Response(
            {"error": "Cart item not found"},
            status=status.HTTP_404_NOT_FOUND
        )



@api_view(['GET'])
def user_list(request):
    users = Register.objects.all()
    serializer = RegisterSerializer(users, many=True)
    return Response(serializer.data)

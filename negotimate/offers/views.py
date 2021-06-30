from django.shortcuts import render
from .models import History, Offer, State
from django.forms.models import model_to_dict
from django.core import serializers
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

@api_view((['POST']))
def submit(request, user_id):

    offer, created = Offer.objects.update_or_create(
        user1_id=user_id,
        user2_id=request.data['user_id'],
        user1_state=State.AWAITING_THEIR_ACCEPTANCE,
        user2_state=State.AWAITING_YOUR_ACCEPTANCE,
        product_name=request.data['product_name'],
        price=request.data['price'],
        quantity=request.data['quantity'],
        version=1
    )

    return Response(status=200, data={"message": "Offer created successfully", "offer_id": offer.id })

@api_view((['PATCH']))
def accept(request, offer_id, user_id):

    offer = Offer.objects.get(pk=offer_id)

    if user_id == offer.user1_id:
        if offer.user1_state == State.AWAITING_YOUR_ACCEPTANCE: 
            offer.user1_state=State.ACCEPTED
            offer.user2_state=State.ACCEPTED
            offer.save()
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user1_state.label}"})

    elif user_id == offer.user2_id:
        if offer.user2_state == State.AWAITING_YOUR_ACCEPTANCE:
            offer.user1_state=State.ACCEPTED
            offer.user2_state=State.ACCEPTED
            offer.save() 
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user2_state.label}"})
    
    else:
        return Response(status=500, data={"message": f"User {user_id} is not recognised for this offer"})

    saveHistory(offer, user_id, 'Accept')

    return Response(status=200, data={"message": "Offer accepted, we hope you got a great deal"})
    
@api_view((['PATCH']))
def cancel(request, offer_id, user_id):

    offer = Offer.objects.get(pk=offer_id)

    if user_id == offer.user1_id:
        if offer.user1_state not in [State.ACCEPTED, State.CANCELLED]: 
            offer.user1_state=State.CANCELLED
            offer.user2_state=State.CANCELLED
            offer.save()
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user1_state.label}"})

    elif user_id == offer.user2_id:
        if offer.user2_state not in [State.ACCEPTED, State.CANCELLED]:
            offer.user1_state=State.CANCELLED
            offer.user2_state=State.CANCELLED
            offer.save() 
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user2_state.label}"})

    else:
        return Response(status=500, data={"message": f"User {user_id} is not recognised for this offer"})

    saveHistory(offer, user_id, 'Cancel')

    return Response(status=200, data={"message": "Offer cancelled, better luck next time.."})
    

@api_view((['PATCH']))
def proposeUpdate(request, offer_id, user_id):

    offer = Offer.objects.get(pk=offer_id)

    if user_id == offer.user1_id:
        if offer.user1_state in [State.WITHDRAWN_BY_ME, State.AWAITING_YOUR_ACCEPTANCE]:
            offer.product_name=request.data['product_name']
            offer.price=request.data['price']
            offer.quantity=request.data['quantity']
            offer.user1_state=State.AWAITING_THEIR_ACCEPTANCE
            offer.user2_state=State.AWAITING_YOUR_ACCEPTANCE
            offer.save()
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user1_state.label}"})

    elif user_id == offer.user2_id:
        if offer.user2_state in [State.WITHDRAWN_BY_ME, State.AWAITING_YOUR_ACCEPTANCE]:
            offer.product_name=request.data['product_name']
            offer.price=request.data['price']
            offer.quantity=request.data['quantity']
            offer.user1_state=State.AWAITING_YOUR_ACCEPTANCE
            offer.user2_state=State.AWAITING_THEIR_ACCEPTANCE
            offer.save()
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user2_state.label}"})
    else:
        return Response(status=500, data={"message": f"User {user_id} is not recognised for this offer"})

    saveHistory(offer, user_id, 'ProposeUpdate')

    return Response(status=200, data={"message": "Offer update, fingers crossed..."})
    
@api_view((['PATCH']))
def withdraw(request, offer_id, user_id):

    offer = Offer.objects.get(pk=offer_id)

    if user_id == offer.user1_id:
        if offer.user1_state in [State.AWAITING_THEIR_ACCEPTANCE]: 
            offer.user1_state=State.AWAITING_YOUR_ACCEPTANCE
            offer.user2_state=State.AWAITING_THEIR_ACCEPTANCE
            offer.save()
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user1_state.label}"})

    elif user_id == offer.user2_id:
        if offer.user2_state in [State.AWAITING_THEIR_ACCEPTANCE]:
            offer.user1_state=State.AWAITING_THEIR_ACCEPTANCE
            offer.user2_state=State.AWAITING_YOUR_ACCEPTANCE
            offer.save()
        else:
            return Response(status=400, data={"message": f"Action not allowed because the state of this offer is: {offer.user2_state.label}"})

    else:
        return Response(status=500, data={"message": f"User {user_id} is not recognised for this offer"})

    saveHistory(offer, user_id, 'Withdraw')
    return Response(status=200, data={"message": "Offer accepted, we hope you got a great deal!"})


@api_view((['GET']))
def getHistory(request, offer_id, user_id):
    histories = History.objects.filter(offer_id=offer_id)
    history_dict = serializers.serialize('json', histories)
    # Would try and convery json to dataframe to print as table
    # df = pd.json_normalize(history_dict)
    # df_2 = df[["fields.offer_id","fields.version"]] 
    # print(history_dict)
    return Response(status=200, data=history_dict)

def saveHistory(offer, user_id, action):
    record = History.objects.create(
        offer_id=offer.id,
        version=offer.version,
        action=action,
        user_id=user_id,
        user1_state=offer.user1_state,
        user2_state=offer.user2_state,
        product_name=offer.product_name,
        buyer=offer.user1_id,
        seller=offer.user2_id,
        price=offer.price
        # private_data=offer.private_data,
    )

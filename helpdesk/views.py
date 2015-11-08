from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

import requests
import xmltodict

class APIError(Exception):
    pass


def sendpayload(payload):
    return requests.post(
        'https://sws3-crt.cert.sabre.com',
        data=payload,
        headers={'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': 'SessionCreateRQ'}
    )


def gettoken(username, password, pcc):
    payload = """<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsd="http://www.w3.org/1999/XMLSchema">
        <SOAP-ENV:Header>
            <eb:MessageHeader SOAP-ENV:mustUnderstand="1" eb:version="1.0">
                <eb:From>
                    <eb:PartyId type="urn:x12.org:IO5:01">999999</eb:PartyId>
                </eb:From>
                <eb:To>
                    <eb:PartyId type="urn:x12.org:IO5:01">123123</eb:PartyId>
                </eb:To>
                <eb:CPAId>IPCC</eb:CPAId>
                <eb:ConversationId>1234</eb:ConversationId>
                <eb:Service>SessionCreateRQ</eb:Service>
                <eb:Action>SessionCreateRQ</eb:Action>
                <eb:MessageData>
                    <eb:MessageId>1000</eb:MessageId>
                    <eb:Timestamp>2001-02-15T11:15:12Z</eb:Timestamp>
                    <eb:TimeToLive>2001-02-15T11:15:12Z</eb:TimeToLive>
                </eb:MessageData>
            </eb:MessageHeader>
            <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext" xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility">
                <wsse:UsernameToken>
                    <wsse:Username>{username}</wsse:Username>
                    <wsse:Password>{password}</wsse:Password>
                    <Organization>{pcc}</Organization>
                    <Domain>DEFAULT</Domain>
                </wsse:UsernameToken>
            </wsse:Security>
        </SOAP-ENV:Header>
        <SOAP-ENV:Body>
            <eb:Manifest SOAP-ENV:mustUnderstand="1" eb:version="1.0">
                <eb:Reference xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="cid:rootelement" xlink:type="simple"/>
            </eb:Manifest>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""
    r = sendpayload(payload.format(username=username, password=password, pcc=pcc))
    parsed = xmltodict.parse(r.text)
    return parsed[u'soap-env:Envelope']['soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']['#text']

def getinfo(uniqueid):
    payload = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsd="http://www.w3.org/1999/XMLSchema">
        <SOAP-ENV:Header>
          <eb:MessageHeader SOAP-ENV:mustUnderstand="1" eb:version="1.0">
             <eb:ConversationId>1234</eb:ConversationId>
             <eb:From>
                <eb:PartyId type="urn:x12.org:IO5:01">99999</eb:PartyId>
             </eb:From>
             <eb:To>
                <eb:PartyId type="urn:x12.org:IO5:01">123123</eb:PartyId>
             </eb:To>
             <eb:Service eb:type="OTA">CDI</eb:Service>
             <eb:Action>TravelItineraryReadRQ</eb:Action>
             <eb:MessageData>
                <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                <eb:Timestamp>2001-02-15T11:15:12Z</eb:Timestamp>
                <eb:TimeToLive>2001-02-15T11:15:12Z</eb:TimeToLive>
             </eb:MessageData>
          </eb:MessageHeader>
          <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext">
             <wsse:BinarySecurityToken valueType="String" EncodingType="wsse:Base64Binary">{token}</wsse:BinarySecurityToken>
          </wsse:Security>
       </SOAP-ENV:Header>
       <SOAP-ENV:Body>
          <TravelItineraryReadRQ Version="3.1.0" TimeStamp="2012-09-19T10:00:00-06:00" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dd="http://webservices.sabre.com/dd2">
             <MessagingDetails>
                <SubjectAreas>
                   <SubjectArea>DEFAULT</SubjectArea>
                </SubjectAreas>
             </MessagingDetails>
             <UniqueID ID="{id}"/>
          </TravelItineraryReadRQ>
       <ns:SessionCreateRQ xmlns:ns="http://www.opentravel.org/OTA/2002/11"><ns:POS/></ns:SessionCreateRQ></SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""
    token = gettoken(1234, 'fdfdfsdfs', 'fafdgsdfgsgsg')
    r = sendpayload(payload.format(token=token, id=uniqueid))
    parsed = xmltodict.parse(r.text)
    try:
        return parsed['soap-env:Envelope']['soap-env:Body']['TravelItineraryReadRS']['TravelItinerary']
    except KeyError:
        error = parsed['soap-env:Envelope']['soap-env:Body']['TravelItineraryReadRS']['stl:ApplicationResults']\
                    ['stl:Error']['stl:SystemSpecificResults']['stl:Message']
        raise APIError('Error {@code} {#text}'.format(**error))


class GetItinerary(TemplateView):
    cache = {}

    def get(self, request, unique_id):
        if unique_id in self.cache:
            info = self.cache.get(unique_id)
        else:
            try:
                info = getinfo(unique_id)
            except APIError as e:
                info = {"error": e.message}
            else:
                self.cache[unique_id] = info

        return render(request, 'helpdesk/info.html', {"info": info, "cache": self.cache})

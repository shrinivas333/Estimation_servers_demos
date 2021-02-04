from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
import json

class CustomApiView(GenericAPIView):
    # required get_object

    serializer_class=None
    model=None
    prefetch=[]
    filter={}
    page_size=10

    search_filter=()

    '''
    desired format is:
     {"search_param_from_url":['attribute1','attribute2']} 
      where attributes are attributed in the database to search for ,for the corresponding search param
    '''
    extra_params_search={}


    __urlEnding=""
    def get(self,request,*args,**kwargs):
        return self.getCustomPaginationResponse(request)

    def get_queryset(self):
        if self.model is not None:
            return self.model.objects.filter()

    def filterSearches(self,queryset):
        d={}
        #for normal search only
        for search in self.search_filter:
            print(search)
            value=self.request.GET.get("search",None)
            if value is not None:
                d[search+"__icontains"]=self.request.GET.get("search","")
                self.__urlEnding +="&{}={}".format(search,self.request.GET.get("search",""))

        print("Normal searches happening",d)
        print(self.extra_params_search)
        for query_key in self.extra_params_search.keys():
            data=self.request.GET.get(query_key,None)
            if data is not None:

                self.__urlEnding +="&{}={}".format(query_key,data)
                for query_location in self.extra_params_search[query_key]:
                    d[query_location+"__icontains"]=self.request.GET.get(query_key,"")

        print("FInal searches happening",d)
        return queryset.filter(**d)



    def __getInitialiData(self):
        queryset = self.get_queryset()
        next = None
        previous = None
        queryset = queryset.order_by("-id").filter(**self.filter)
        queryset=self.filterSearches(queryset)[:self.page_size+1]
        length = len(queryset)
        if length != 0 and length>self.page_size:
            next = self.request.scheme + "://" + self.request.get_host() + self.request.path + "?fromId=" + str(
                queryset[length - 1].id)+self.__urlEnding

        serialized_data = self.serializer_class(queryset, many=True)
        output = {}
        data = json.loads(JSONRenderer().render(serialized_data.data))
        output['previous'] = previous
        output['next'] = next
        output['results'] = data
        return JsonResponse(output, json_dumps_params={'ensure_ascii': False})
    
    def __getNextData(self,fromId):
        queryset = self.get_queryset()
        next = None
        previous = None
        queryset = queryset.order_by("-id").filter(**self.filter).filter(id__lt=fromId)
        queryset=self.filterSearches(queryset)[:self.page_size+1]

        length = len(queryset)
        if length != 0:
            #check if there is required to be a next
            if length==self.page_size+1:
                next = self.request.scheme + "://" + self.request.get_host() + self.request.path + "?fromId=" + str(
                    queryset[length - 2].id)+self.__urlEnding
            previous = self.request.scheme + "://" + self.request.get_host() + self.request.path + "?beforeId=" + str(
                queryset[0].id)+self.__urlEnding
        else:
            previous = self.request.scheme + "://" + self.request.get_host() + self.request.path + "?beforeId=" + str(int(fromId) - 1)+self.__urlEnding
        serialized_data = self.serializer_class(queryset, many=True)
        output = {}
        data = json.loads(JSONRenderer().render(serialized_data.data))
        output['previous'] = previous
        output['next'] = next
        output['results'] = data[:self.page_size]
        return JsonResponse(output)

    def __getPreviousPage(self,beforeId):
        queryset = self.get_queryset()
        next = None
        previous = None
        queryset = queryset.order_by("id").filter(**self.filter).filter(id__gt=beforeId)
        queryset=self.filterSearches(queryset)[:self.page_size+1]

        serialized_data = self.serializer_class(queryset, many=True)
        output = {}
        data = json.loads(JSONRenderer().render(serialized_data.data))
        data.reverse()

        length = len(queryset)
        if length==self.page_size+1:
            data = data[1:]

        if length != 0:

            if length == self.page_size+1:
                #this case occurs if there is a previous data post this action
                previous = self.request.scheme + "://" + self.request.get_host() + self.request.path + "?beforeId=" + str(
                    data[0]['id'])+self.__urlEnding
            next = self.request.scheme + "://" + self.request.get_host() + self.request.path + "?fromId=" + str(
                data[len(data)-1]['id'])+self.__urlEnding

        else:
            next = self.request.scheme + "://" + self.request.get_host() + self.request.path+"?"+self.__urlEnding

        output['previous'] = previous
        output['next'] = next
        output['results'] = data[:self.page_size]
        return JsonResponse(output)

    def getCustomPaginationResponse(self,request):
        fromId=self.request.GET.get("fromId",None)
        beforeId=self.request.GET.get("beforeId",None)
        queryset=self.get_queryset()
        next=None
        previous=None
        

        #trying to fetch queryset from get_object
        #note data is always ordered in reverse format so that latest information is displayed first
        #case default data without from or last where the top data has to be displayed
        #case frorm id set, display next set of data from  that particular id onwards
        #case before id set, display previous set of data which happened before that id

        if fromId is None and beforeId is None:
            return self.__getInitialiData()
            # #case default data withotu from or last where top data has to be displayed
            # queryset=queryset.order_by("-id").filter(**self.filter)[:self.page_size]
            # length=len(queryset)
            # if length!=0:
            #     next = request.scheme + "://" + request.get_host() + request.path + "?fromId=" + str(queryset[length-1].id)
        elif fromId is not None:
            return self.__getNextData(fromId)
            # queryset=queryset.order_by("-id").filter(**self.filter).filter(id__lt=fromId)[:self.page_size]
            # length = len(queryset)
            # if length != 0:
            #     next = request.scheme + "://" + request.get_host() + request.path + "?fromId=" + str(
            #         queryset[length - 1].id)
            #     previous = request.scheme + "://" + request.get_host() + request.path + "?beforeId=" + str(
            #         queryset[0].id)
            # else:
            #     previous = request.scheme + "://" + request.get_host() + request.path + "?beforeId=" + str(int(fromId)-1)
        else:
            #before Id is probably given
            # queryset = queryset.order_by("id").filter(**self.filter).filter(id__gt=beforeId)[:self.page_size]
            # length = len(queryset)
            # if length != 0:
            #     next = request.scheme + "://" + request.get_host() + request.path + "?fromId=" + str(
            #         queryset[length - 1].id)
            #     previous = request.scheme + "://" + request.get_host() + request.path + "?beforeId=" + str(
            #         queryset[0].id)
            # else:
            #     next = request.scheme + "://" + request.get_host() + request.path
            return self.__getPreviousPage(beforeId)





        serialized_data=self.serializer_class(queryset,many=True)
        output={}
        data=json.loads(JSONRenderer().render(serialized_data.data))
        output['previous']=previous
        output['next']=next
        output['results']=data
        return JsonResponse(output)
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,  HttpResponseRedirect,JsonResponse
from .models import Question
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Tags,  Choice
import json
from django.core import serializers

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#     # template = loader.get_template('polls/index.html')
#     # context = {
#     #     'latest_question_list' : latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))
#     # print(latest_question_list)
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)

    


# def detail(request,question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, 'polls/details.html',{'question': question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist :
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/details.html',{'question' : question})
#     # return HttpResponse("You're looking at question %s."% question_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/details.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'




def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
@csrf_exempt
def api1(request):
    if request.method == 'POST':
        # Parse the request data 
        #Convert the data to python dictionary
        request_data = json.loads(request.body)
        print(request_data)
        question = request_data.get('Question')
        option_vote = request_data.get('OptionVote')
        tags = request_data.get('Tags')
        
        
        # question = Question(question_text = question)
        # question.save()
        print(question)
        print(option_vote)
        print(tags)

        #create question object
        question = Question(question_text = question)
        question.save()

        #Create vote objects
        for x,y in option_vote.items():
            option = Choice(question = question, choice_text = x, votes=y)
            option.save()

        for x in tags:
            tag = Tags(question=question,name=x)
            tag.save()

        # Return a JSON response
        response_data = {'message': 'Success'}
        return JsonResponse(response_data)

@csrf_exempt
def api2_get(request):
    if request.method == 'GET':
        data = Question.objects.all()
        final = []

        for x in data:
            dict_res = {
                'id': x.id,
                'Question': x.question_text,
                'OptionVote': {},
                'Tags': []
            }
            
            choices = Choice.objects.filter(question=x)
            for choice in choices:
                dict_res['OptionVote'][choice.choice_text] = choice.votes

            tags = Tags.objects.filter(question=x)
            for tag in tags:
                dict_res['Tags'].append(tag.name)

            final.append(dict_res)

        return JsonResponse(final, safe=False)
    


@csrf_exempt
def tag_check(request, tag_names):
    if request.method == 'GET':
        print('Inside function')
        tag_list = tag_names.split(',')
        print(tag_list)
        final = []
        for tag_name in tag_list:
            tag = Tags.objects.get(name=tag_name)
            primary = tag.question
            result = {
                'id': primary.id,
                'Question': primary.question_text,
                'OptionVote': {},
                'Tags': []
            }

            choice_obj = Choice.objects.filter(question=primary)
            for choice in choice_obj:
                result['OptionVote'][choice.choice_text] = choice.votes

            tag_object = Tags.objects.filter(question=primary)
            for tag_obj in tag_object:
                result["Tags"].append(tag_obj.name)

            final.append(result)

        print(final)
        return JsonResponse(final, safe=False)


@csrf_exempt
def update_poll(request,id):
    if request.method == 'PUT':
        request_data = json.loads(request.body)
        option = request_data.get('incrementOption')
        print(option)
        print(option)
        try:
            chk = 0
            res = Question.objects.get(pk=id)
            try:
                choices = Choice.objects.filter(question=res)
                for x in choices:
                    print(x.choice_text)
                    if x.choice_text == option:
                        print('Found')
                        x.votes += 1
                        x.save()
                        chk = 1
                        print(x.votes)
                if chk == 0:
                    return JsonResponse({'Error':'No such choice for the given id'})
                
                
            except Choice.DoesNotExist:
                return JsonResponse({'error':'No choices for the given question'})
        except Question.DoesNotExist:
            return JsonResponse({'error':'Invalid poll number'})

        final = 'Poll updated Successfully'
        print(final)
        return JsonResponse(final, safe=False)
    

@csrf_exempt
def get_poll(request,pk):
    if request.method == 'GET':
        final = []
        try:
            res = Question.objects.get(pk=pk)
            result = {
                "Question": res.question_text,
                "OptionVote":{
                },
                "Tags": []
            }
            choices = Choice.objects.filter(question=res)
            for x in choices:
                result['OptionVote'][x.choice_text]=x.votes

            tags = Tags.objects.filter(question=res)
            for x in tags:
                result['Tags'].append(x.name)

            final.append(result)
            print(final)
        except Question.DoesNotExist:
            return JsonResponse({'error':'Invalid poll number'})
        return JsonResponse(result,safe=False)


@csrf_exempt
def get_tag(request):
    if request.method == 'GET':
        result = {
            "Tags":[]
        }
        li = Tags.objects.values('name')
        tag_names=[]
        for x in li:
            tag_names.append(x['name'])
        for x in tag_names:
            result['Tags'].append(x)
        return JsonResponse(result,safe=False)
        

@csrf_exempt
def get_question_id(request, question_text):
    question = get_object_or_404(Question, question_text=question_text)
    question_id = question.id
    return JsonResponse({'question_id': question_id})


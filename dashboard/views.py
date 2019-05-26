from django.shortcuts import render, get_object_or_404
import plotly
import plotly.graph_objs as go
from .models import Project, Attribute, Field, Criterion
from django.http import HttpResponseRedirect
import datetime

def index(request):
	projects = Project.objects.all()
	return render(request, "index.html", {'projects':projects})

def new(request):
	if request.method == "POST":
		project = Project(name=request.POST.get("name"), date_created=datetime.datetime.now())
		project.save()
		return HttpResponseRedirect("/projects/view/{}".format(project.id))
	else:
		return render(request, 'new.html')

def view(request, id):
	project = get_object_or_404(Project, pk=id)
	criteria = project.criteria.all()
	theta = [attribute.name for attribute in Attribute.objects.all()]
	r = []
	results = {}
	for attribute in theta:
		criterion = list(filter(lambda c:c.question.field.name == attribute, criteria))
		r_sum = 0
		weight_sum = 0
		for c in criterion:
			weighting = c.question.weighting
			r_sum += (c.rating * weighting)
			weight_sum += weighting
		r.append(r_sum/weight_sum) if weight_sum != 0 else r.append(0)
	total_sum = sum(r)
	average = total_sum / len(r)
	below_average = []
	for value, attribute in zip(r, theta):
		if value < average:
			below_average.append(attribute)
	results["below_average"] = below_average
	MAX = 5
	area = 0
	i = 0
	r.append(r[0])
	theta.append(theta[0])
	while i < len(theta) - 1:
		sub_area = (r[i] * r[i+1])/2
		area += sub_area
		i += 1
	max_area = (len(theta) - 1) * ((MAX * MAX)/2)
	score = round((area / max_area) * 100, 1)
	results["score_class"] = get_score_class(score)
	results["score"] = score
	data = [go.Scatterpolar(
		r = r,
		theta = theta,
		fill = 'toself'
	)]

	layout = go.Layout(
	polar = dict(
		radialaxis = dict(
		visible = True,
		range = [0, 5]
		)
	),
	showlegend = False,
	height = 600,
	margin = dict(
		t = 30,
		l = 10
	)
	)

	fig = go.Figure(data=data, layout=layout)
	graph = plotly.offline.plot(fig, output_type='div', show_link=False, config={"displayModeBar":False})

	return render(request, 'view.html', {'project':project,'graph': graph, 'results' : results})

def enter_data(request, id):
	project = get_object_or_404(Project, pk=id)
	if request.method == "POST":
		values = dict(request.POST)
		del values['csrfmiddlewaretoken']
		for c in project.criteria.all():
			project.criteria.remove(c)
		for key, value in values.items():
			field = get_object_or_404(Field, pk=key)
			criterion = get_object_or_404(Criterion, question=field, rating=int(value[0]))
			criterion.projects.add(project)
		return HttpResponseRedirect("/projects/view/{}".format(project.id))
	else:
		attributes = Attribute.objects.all()
		criteria = project.criteria.all()
		return render(request, 'enter_data.html', {'project':project, 'attributes' : attributes, 'criteria' : criteria})

def get_score_class(score):
	if score <= 20:
		return "badge-danger"
	elif score <= 30:
		return "badge-warning"
	elif score <= 50:
		return "badge-info"
	elif score <= 80:
		return "badge-primary"
	else:
		return "badge-success"
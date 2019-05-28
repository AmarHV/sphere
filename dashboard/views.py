from django.shortcuts import render, get_object_or_404
import plotly
import plotly.graph_objs as go
from .models import Project, Attribute, Field, Criterion, Category
from django.http import HttpResponseRedirect
import datetime

def index(request):
	projects = Project.objects.all()
	results = {}
	for project in projects:
		r, theta = get_graph_data(project)
		stats = get_stats(r, theta, project.category, project)
		results[project] = stats
	return render(request, "index.html", {'projects':projects, 'results': results})

def new(request):
	if request.method == "POST":
		category = get_object_or_404(Category, pk=request.POST.get('category'))
		project = Project(name=request.POST.get("name"), date_created=datetime.datetime.now(), category=category)
		project.save()
		return HttpResponseRedirect("/projects/view/{}".format(project.id))
	else:
		categories = Category.objects.all()
		return render(request, 'new.html', {"categories":categories})

def view(request, id):
	project = get_object_or_404(Project, pk=id)
	r, theta = get_graph_data(project)
	results = get_stats(r, theta, project.category, project)
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

def get_graph_data(project):
	criteria = project.criteria.all()
	theta = [attribute.name for attribute in Attribute.objects.all()]
	r = []
	for attribute in theta:
		criterion = list(filter(lambda c:c.question.field.name == attribute, criteria))
		r_sum = 0
		weight_sum = 0
		for c in criterion:
			weighting = c.question.weighting
			r_sum += (c.rating * weighting)
			weight_sum += weighting
		r.append(r_sum/weight_sum) if weight_sum != 0 else r.append(0)
	return (r, theta)

def get_stats(r, theta, project_category, project):
	results = {}
	weightings = project_category.category_attribute_weightings.all()
	weighting_sum = 0
	for weighting in weightings:
		weighting_sum += weighting.weighting
	total_sum = sum(r)
	average = total_sum / len(r)
	below_average = {}
	for value, attribute in zip(r, theta):
		if value < average:
			below_average[attribute] = list()
			for question in Attribute.objects.filter(name=attribute)[0].fields.all():
				if project.criteria.filter(question=question)[0].rating <= value:
					below_average[attribute].append(question.improvement_message)
	results["below_average"] = below_average
	MAX = 5
	area = 0
	i = 0
	r.append(r[0])
	theta.append(theta[0])
	while i < len(theta) - 1:
		weighting_0 = list(filter(lambda x: x.attribute.name == theta[i], weightings))[0]
		area += r[i]*weighting_0.weighting
		i += 1
	area = area / (len(theta) - 1)
	val = 0
	i = 0
	while i < len(theta) - 1:
		weighting_0 = list(filter(lambda x: x.attribute.name == theta[i], weightings))[0]
		val += weighting_0.weighting*MAX
		i += 1
	max_area = val / (len(theta) - 1)
	score = round((area / max_area) * 100, 1)
	results["score_class"] = get_score_class(score)
	results["score"] = score
	return results
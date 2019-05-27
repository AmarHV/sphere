from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Attribute(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class CategoryAttributeWeighting(models.Model):
	category = models.ForeignKey(Category, related_name='category_attribute_weightings', on_delete=models.CASCADE)
	attribute = models.ForeignKey(Attribute, related_name='category_attribute_weightings', on_delete=models.CASCADE)
	weighting = models.FloatField()
	def __str__(self):
		return "{}/{}".format(self.category, self.attribute)

class Project(models.Model):
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category, related_name='projects', on_delete=models.PROTECT, null=True)
	date_created = models.DateTimeField()
	def __str__(self):
		return self.name

class Field(models.Model):
	question = models.CharField(max_length=500)
	weighting = models.FloatField()
	field = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="fields")
	def __str__(self):
		return self.question

class Criterion(models.Model):
	question = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="criteria")
	projects = models.ManyToManyField(Project, related_name="criteria", blank=True)
	rating = models.IntegerField()
	description = models.TextField()
	def __str__(self):
		return "{} - {:.50s}".format(self.rating, self.description)
	class Meta:
		ordering = ['rating']
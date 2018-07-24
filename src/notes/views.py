# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from .models import Entry
from .forms import EntryModelForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def entry_list(request):
	all_entries=Entry.objects.filter(user=request.user)
	query=request.GET.get("q")
	if query:
		all_entries=all_entries.filter(Q(title__icontains=query))   		#iexact, icontains
	context={
		'object_list':all_entries
	}
	return render(request, "notes/entries.html", context)


@login_required
def entry_detail(request, id):
	note = get_object_or_404(Entry, id=id)
	context={
		'object': note
	}
	return render(request, "notes/entries_detail.html", context)


@login_required
def entry_create(request):
	form=EntryModelForm(request.POST or None, request.FILES)
	if form.is_valid():
		form.instance.user = request.user
		form.save()
		entry_id=form.instance.id
		entry=get_object_or_404(Entry, id=entry_id)
		messages.info(request, 'Created a new note!')
		return redirect(entry.get_absolute_url())
	context={
		'form': form
	}
	return render(request, "notes/entries_create.html", context)


@login_required
def entry_update(request, id):
	instance = get_object_or_404(Entry, id=id)
	form=EntryModelForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		form.save()
		entry_id=form.instance.id
		entry=get_object_or_404(Entry, id=entry_id)
		return redirect(entry.get_absolute_url())
	context={
		'form':form,
		'instance': 'object'
	}
	return render(request, "notes/entries_update.html", context)

@login_required
def entry_delete(request, id):
	instance=get_object_or_404(Entry, id=id)
	if instance.user!=request.user:
		response = HttpResponse("You don't have permission to delete this.")
		response.status_code=403
		return response

	if request.method == "POST":
		instance.delete()
		messages.info(request, "This note has been successfully deleted!")
		return redirect("/entries/")
	context={
		'object': instance
	}
	return render(request,"notes/entries_delete.html", context)


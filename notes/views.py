from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from notes.models import Note, Image, DisplayMode
from django.utils import timezone
from django.http import HttpResponse
from .forms import ImageUploadForm
from .search_module import search_note, create_regex_pattern
import sys

def make_new_note():
    while True:
        empty_notes = Note.objects.filter(note_text__lt=1)
        if len(empty_notes) > 0:
            break
        else:
            Note.objects.create(note_text='')
            continue

class HomeView(generic.ListView):
    """Generates the home view"""

    template_name = 'notes/home.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(note_text__gt=0, date_created__lte=timezone.now()).order_by('-last_updated')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        empty_notes = list(Note.objects.filter(note_text=''))
        if len(empty_notes) == 0:
            Note.objects.create(note_text='')
        context['theme'] =  DisplayMode.objects.get(pk=1).display_mode
        context['empty_note'] = list(Note.objects.filter(note_text=''))[-1]
        context['error_message_enter_text'] = 'Please enter some text'
        context['error_message_no_search_results'] = 'No search results found😗'

        return context

def change_display_mode(request, display_mode_index):
    modes = ['light-mode', 'dark-mode']
    DisplayMode.objects.filter(pk=1).update(display_mode=f"{modes[display_mode_index]}")
    return HttpResponseRedirect(reverse('notes:home'))

def search_notes(request):
    make_new_note()
    context = {
        'notes': Note.objects.filter(note_text__gt=1, date_created__lte=timezone.now()).order_by('-last_updated'),
        'error_message_enter_text': 'Please enter some text',
        'error_message_no_search_results': 'No search results found😗',
        'empty_note': list(Note.objects.filter(note_text=''))[-1],
    }

    if request.method == 'POST':
        query_val = request.POST['q']
        if(query_val != ''):
            notes = Note.objects.filter(note_text__iregex=rf"{create_regex_pattern(query_val)}").order_by('-last_updated')
            for note in notes:
                note.note_text = search_note(query_val, note.note_text)
            context['notes'] = notes

    return render(request, 'partials/results.html', context)


class NoteView(generic.DetailView):
    model = Note
    template_name = 'notes/note.html'

    def get_queryset(self):
        return Note.objects.filter(date_created__lte=timezone.now())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] =  DisplayMode.objects.get(pk=1).display_mode
        context['form'] = ImageUploadForm()
        return context


def new_note(request, colour_theme):
    empty_notes = Note.objects.filter(note_text__lt=1)
    if len(empty_notes) == 0:
        Note.objects.create(note_text='')
        empty_notes = Note.objects.filter(note_text__lt=1)


    empty_notes.update(colour_theme=colour_theme, date_created=timezone.now())

    return render(request, 'notes/note.html', context={
        'note': empty_notes[0],
        'theme': DisplayMode.objects.get(pk=1).display_mode
    })


def change_colour(request, pk, colour_theme):
    Note.objects.filter(pk=pk).update(colour_theme=f"{colour_theme}-theme")
    return HttpResponseRedirect(reverse('notes:note', args=[pk]))


def delete_note(request, pk):
    Note.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('notes:home'))


def update(request, pk):
    if request.method == 'POST':
        new_text = request.POST['note']
        Note.objects.filter(pk=pk).update(note_text=new_text, last_updated=timezone.now())
        return HttpResponse("It's alive")
    
def add_image(request, pk):
    if request.method == 'POST':
        file = request.FILES['new_image']   
        note = Note.objects.get(pk=pk)
        Image.objects.create(note=note, image=file)
        Note.objects.filter(pk=pk).update(last_updated=timezone.now())

    return HttpResponseRedirect(reverse('notes:note', args=[pk]))

def images(request, pk, image_index):
    context = {}
    images = Note.objects.get(pk=pk).image_set.all()
    context['note'] = Note.objects.get(pk=pk)
    context['images'] = images
    context['current_index'] = image_index
    context['current_image'] = images[image_index]
    if image_index + 1 < len(images):
        context['previous_image'] = images[image_index + 1]
        context['previous_image_index'] = image_index + 1
    if image_index - 1 >= 0:
        context['next_image'] = images[image_index - 1]
        context['next_image_index'] = image_index - 1

    context['display_mode'] = DisplayMode.objects.get(pk=1).display_mode

    return render(request, 'notes/image_gallery.html', context)

def delete_img(request, pk, image_index, image_pk):
    images = Note.objects.get(pk=pk).image_set.all()
    images.get(pk=image_pk).delete()
    Note.objects.filter(pk=pk).update(last_updated=timezone.now())
    return HttpResponseRedirect(reverse('notes:note', args=[pk])) 


def gallery_deletion(index, images):
    """Simulates an image gallery's next item to be shown when one image is deleted"""
    images = list(images)
    new_index = index
    next_images = images[index + 1:]
    previous_images = images[: index]

    try:
        images[index]
    except IndexError:
        print("Didn't work son") # this isnt expected to happen
        sys.exit()
        
    if len(previous_images) > 0:
        new_index = index - 1
    elif len(next_images) > 0:
        new_index = index
    elif [images[index]] == images:
        return None
    
    del images[index]

    return new_index


def delete_img_from_gal(request, pk, image_index, image_pk):
    images = Note.objects.get(pk=pk).image_set.all()
    new_index = gallery_deletion(image_index, images)
    images.get(pk=image_pk).delete()
    Note.objects.filter(pk=pk).update(last_updated=timezone.now())
    if not(new_index == None):
        return HttpResponseRedirect(reverse('notes:images', args=[pk, new_index]))
    else:
        return HttpResponseRedirect(reverse('notes:note', args=[pk]))

def describe(request, pk, image_index, image_pk):
    current_image = Note.objects.get(pk=pk).image_set.all().filter(pk=image_pk)
    new_text = request.POST['alt_text']
    current_image.update(alt_text=new_text)
    print('yuh')
    return HttpResponseRedirect(reverse('notes:images', args=[pk, image_index]))
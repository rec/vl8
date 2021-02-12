🔉 vl8: Create derivative works that might not be copyright violations 🔉
----------------------------------------------------------------------------

.. image:: https://raw.githubusercontent.com/rec/vl8/master/vl8.png
   :alt: vl8 logo

A command line tool and Python library that (will soon be) like a Swiss Army
Knife for audio.

* Create a myriad of mashups of your favorite audio effortlessly.

* Script mundane tasks like editing, scaling and stretching, envelopes,
  playlists and more.

* Handle very large audio files using memory mapping, or very large numbers of
  audio files using scripting.

* Write your own scripts for mashups or editing, or your own plug-ins, and
  share them.

* Uses widely compatible, highly performant numpy arrays to represent audio
  files within Python.


 Typical command lines:

     vl8 one.wav  # Info on the file.
     vl8 cat one.wav two.wav three.wav  # concatenates them
     vl8 'cat(gap=2)' one.wav two.wav   # concatenate them with no gap
     vl8 'cat(gap=2)' one.wav two.wav --out=three.wav
     vl8 'cat(gap=2)' one.wav two.wav 'rubberband(pitch=-50)'
     ###  vl8 mix reverse one.wav NO.
     vl8 'reverse(balance=0.5)' one.wav  # balance!
     vl7 'slice(length=[2, 3], duration=12, maxslice=4)' one.wav two.wav
     vl7 'sample(jump=4, length=1, count=20)' one.wav two.wav

"Balance" is a special case where we mix the input with the output.  We want to
do that a lot of the time.

If a function doesn't have a balance command, we put it in for them
automatically.

Problem: automatically creating the output name
Answer: a timestamp with add the base names of all the effects appended


If we write multiple files, they all get the same timestamp and a changing index
number:

   2021.02.23-08.23.35-reverse-cat-1.wav
   2021.02.23-08.23.35-reverse-cat-2.wav
   2021.02.23-08.23.35-reverse-cat-3.wav

(even if writing take

The grammar

Each non-flag token is either an audio file or a command.  Audio files end with
.wav or some other audio thing.

(In this example, functions are lower case - g, f, h.  Files are upper case: A,
B, C.)

f A B same as A f B or A B f

f A B g -> OK

f A B g C D ?

I guess we add these sources into the list of sources.


_Two_ sorts of functions:

singles: single-valued functions that return a single file.
multis: multiple-valued functions that return one or more files.

A single is naturally a multi by applying it to each source individually.

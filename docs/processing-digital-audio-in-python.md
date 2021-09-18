# A plan for a system to process digital audio in Python

## Summary

You can use Python numpy processors, Pedalboards, and external binaries like
ffpmeg, within one Python program, and manage not to have to learn about
most of it.


## Introduction: why DSP in Python?

You can skip to the next section if you want to get to the new material!

Dense, continuous streams of data like audio and video have both challenged
and rewarded programmers since the dawn of the computer age.

Once upon a time audio was eight-bit and we wrote assembly language programs
that occupied kilobytes of memory and ran on a single processor with
sub-megahertz clock speeds.  Doing even a little was very hard.

Languages that compiled to machine language like C, and later, C++ took over
audio processing, because they offered increasingly high-level views of the
world and, well, a lot less typing!, but also the ability to see high-level
structures that would simply have been lost writing in assembly language.

It's hard to quantify how much less work it is to write modern C++ (or Rust,
or any modern language, but C++ is 95% of digital audio processing) over
1981-vintage PDP-11 machine language, but if you factor in the availability
of high quality libraries already written to do the heavy lifting, it would
have to be two or three orders of magnitude - one hundred to one thousand
times less work, maybe even less than that.

However, compiled languages are still hard on the programmer. To get the
"pedal to the metal" performance of C++, the language does not enforce
flanges and guards that protect your programmer fingers from getting burnt,
and then you need to spend years of your life learning a discipline - how not
to burn your fingers in a large number of ways. It's my belief that this is
less true of another compiled language, Rust, but these are still weighty
languages.

You saw it coming, but enter Python.

I'm going to skip the paens to the elegance and simplicity of this language,
but for literally millions of people, the fact being "handy with computers"
lets you write useful Python programs almost immediately is an irresistable
feature.

A compiled language puts together source code into a binary, which cannot(*)
change.

But the Python interpreter sits motionless, like a spider in the center of
its web, and dynamically loads both other Python code, and C or C++ code
as you command.

This is how Python can have its excellent
[REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) -
the "Python shell" where you type in Python commands and see results
immediately. This feature alone is hard to beat for the casual tinkerer, or
the rapid developer at any level.

Originally, Python was an unlikely choice for DSP code, because all that
flexibility comes with a tremendous cost in raw speed - a pure Python program
might be anywhere from roughly 3 to 100 times as slow as "the same" program
written in a compiled language.

Enter numpy, a Python library that allows you to perform computations on
collections of numbers with (more or less) the speed of compiled code.

Years ago, I wrote a project to render a long sample using classic Python,
and set it off. It took 14 hours to run. Then I rewrote it in numpy. It took
less than ten minutes to run, a speedup of over 80x.

-----

(* - yes, dynamically  loaded libraries are a thing, but you know what I mean)

## Pedalboard

Recently Spotify released a Python library called "Pedalboard" which allows
you to run either JUCE filters or - amazingly! - VST or AU processors from
within Python, by running them on `numpy` arrays.

Your Python program constructs a `Pedalboard`, adds `Plugins` to it, and then
calls `Pedalboard.process()` on the `numpy` array that you got from loading
your audio file.

`Plugins` have "parameters" on them which are set when they are constructed
and cannot be varied over the run of the process.


## From Pedalboard to a universal plug - the Processor.

Pedalboard's interface is simple and clear but is not very expressive.

What about a universal plug - call it a Processor?

Let's try to keep as much simplicity as possible, while making it general
enough to represent any processing operation you might conceive of!

### Step 0

Here's `pedalboard.process()`. Don't worry if some of the Python is
unfamiliar to you, just squint a bit to get the big picture.

    def process(
        self,
        audio: np.ndarray,
        sample_rate: Optional[float] = None,
        buffer_size: Optional[int] = None,
    ) -> np.ndarray:

Your sample is fed in as `audio`, and then a brand-new sample is returned
when the process is completed.

### Step 1

Now, I don't really know what `buffer_size` is, because `audio` _has_ a
size!, and there will be more "random" arguments like this, so let's start by
extracting out all of them as `meta`.

    def process(audio: np.ndarray, meta: Dict) -> np.ndarray:

### Step 2

 Suppose we want to chop a big sample into little ones!
So we would like the output to be zero or more arrays:

    def process(audio: np.ndarray, meta: Dict) -> List[np.ndarray]:

### Step 3

Next we want to mix two or more samples or have a synthesizer which takes
_no_ inputs:

    def process(ins: List[np.ndarray], meta: Dict) -> List[np.ndarray]:

### Step 4

Now we'd like to be able to _overwrite_ samples, not just to save memory but
also to save CPU time and avoid thrashing memory with a lot of memory
allocation/deallocation pairs.

    def process(
        ins: List[np.ndarray], outs: List[np.ndarray], meta: Dict
    ) -> List[np.ndarray]:

### Step 5

We're not done yet though.

We have only two places to configure things: we can set parameters when we
construct our DSP parts (like Pedalboard `Plugin`s), or we can pass meta
values in.

But what if we want values that change over time like envelopes, fades and
crossfades, LFOs?

Let's call these "control signals". This is a huge bucket of worms, so let's
just give it a name and make it optional for now:

    def process(
        ins: List[np.ndarray],
        outs: List[np.ndarray],
        meta: Dict,
        control: Optional[ControlSignals] = None,
    ) -> List[np.ndarray]:

### Step 6

And one more change.

Suppose we want to write a program that analyzes a sample and returns a
control signal from it - say, an amplitude envelope.

Then we need to optionally _return_ a `ControlSignal`, like this:

    def process(
        ins: List[np.ndarray],
        outs: List[np.ndarray],
        meta: Dict,
        control: Optional[ControlSignals] = None,
    ) -> Union[List[np.ndarray], ControlSignals]:

And this time, we really are done.  Right?


## Restrictions and adaptors

Yes, we are!

That generalized `process` interface is going to be the "universal plug".
We're going to glue together a lot of things that have `.process()` methods
and make them do tricks for us.

But we need to make it easier to use.

This does represent a lot of digital audio computations, but it's not just
wordy for simple applications, it makes it easy to make mistakes.

You're experimenting and you look at a very simple operation - change
a single sample's amplitude inline, without creating a new sample.

You really want a plain old function like this:

    def scale(out: np.darray, mult: float=0.5) -> None:
         out *= mult

What could be finer?

But instead you have to create a class, and use that gnarly interfaces above
and put in comments.  It's horrible:

    class Scale:
        def process(
            ins: List[np.ndarray],  # Don't use this!
            outs: List[np.ndarray],  # Exactly one here
            meta: Dict,  # 'mult', default = 0.5
            control: Optional[ControlSignals] = None,  # Do not use
        ) -> Union[List[np.ndarray], ControlSignals]:
            out = outs[0]
            return [out *= meta.get('mult', 0.5)]

Everyone's eyes are bleeding by the end,

Luckily, we can take this chore away from you, the experimenter, because
Python has reflection capabiliities - it can look into its own structures
like a hominin looking into a mirror.

The original function or class, in this case `scale()` is called a
_Restriction_, because it accepts a restricted subset of the arguments to a
full `process()`.

Reflection on the Restriction is used to create an _Adaptor_ with a full
`process()` method.

It's much harder to call things wrong, and if you do, you will get better
error checking and reporting.

## Mutators, Creators, and Simple Processors

A Processor which changes existing `np.darray`'s (in `outs`) is a Mutator
and one that creates new `np.darray`s instances is a Creator. One
Processor can be one or the other or both at different times.

A Simple Processor operates on a single sample either as a Mutator or a Creator.

All `Pedalboard`s are Simple Creators.

A Simple Processor can be _multiplexed_ to used it on a collection of
samples, returning a collection of samples (if it's a Creator).


## Split up the Processor class

There are actually two somewhat different things glued together in the
Processor which mention.

One of these is the Description of the computation we want to perform.

Creating a computation Description should be very "light" and you should be
able to create static class instances without causing any allocation.

These are intended to be Python dataclasses or something very similar like
attrs.

The other is the State of the computation. Just getting this State set up to
perform a computation might involve some considerable resources expended. And
the actual computation might be long enough you wanted to track its progress.

Often behind the scenes the Processor Description will create a State which
takes the Description and runs the computation.

All the configuration information goes on the Description, all the mutability
in the State.

# Glueing together processors easily

TBD: there's a lot of code in vl8 to do this but I'll have to look into it.

# External Processors

These are Processors that wrap an executable like `ffmpeg` or `avconf` which
operate on disk file, so they can work on `np.ndarray`s - like
[this](https://github.com/rec/vl8/blob/master/vl8/dsp/external.py).

# What next?

There's lots more to write in English but I think a lot of code is in order.

I have a lot of DSP code already written - I need to put it into the above
framework!

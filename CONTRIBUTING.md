# How to contribute

I'm really glad you're reading this, because i am happy for any help this project come to fruition.
We want you working on things you're excited about.

Here are some important resources:

  * [TU Graz, Institute of Medical Engineering Website](https://www.tugraz.at/institute/ibi/research/nuclear-quadrupole-resonance/) tells you what the Projekt is about, and what it is based on
  * [Pulsed and continuous-wave magnetic resonance spectroscopy using a low-cost software-defined radio](https://aip.scitation.org/doi/10.1063/1.5127746) 
  * [Software Defined Radio based Nuclear Quadrupole Resonance Spectrometer](www.tugraz.at)

## Testing

Before a pull request do a comprehensive test of you changes on the software.

## Submitting changes

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

## Coding conventions

Start reading our code and you'll get the hang of it. It is optimized for readability:

  * For indentation use four spaces in place of soft tabs
  * We avoid logic in views, putting HTML generators into helpers
  * ALWAYS put spaces after list items and method parameters (`[1, 2, 3]`, not `[1,2,3]`), around operators (`x += 1`, not `x+=1`), and around hash arrows.
  * This is open source software. Consider the people who will read your code, and make it look nice for them. It's sort of like driving a car: Perhaps you love doing donuts when you're alone, but with passengers the goal is to make the ride as smooth as possible.
  * So that images can be easily globaly updated, always use image_path or image_tag when referring to images. Never prepend "/images/" when using image_path or image_tag.
  * Also always use cwd-relative paths rather than root-relative paths in image URLs in any CSS. So instead of url('/images/blah.gif'), use url('../images/blah.gif').

Thanks,

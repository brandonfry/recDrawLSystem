# recDrawLSystem

I was working through www.interactivepython.org 's algorithms and data structures course and hit a couple exercises to recursively draw various Lindenmayer system curves. I decided to go full Month and just build a script to recursively draw any aribitrary L-system curve.

As of now the program works for most any input and, by default, prints out a small Sierpinski triangle. Turtle is used to handle the graphics. Input checks and parsing are done by regex. 

The one bit of functionality not baked in at the moment is the handling of parentheses. Parens can be used in L-systems to denote when the curve should back-track to a previous branching-off point. This is useful for making tree shapes and the like. I suppose it would be easy to either add that to the Point class, tracking previous save points in a stack until needed. Alternatively it could be done in recGenerateLString by simply going backwards in the set of instructions after reaching a closing paren. 

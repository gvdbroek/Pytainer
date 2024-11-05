
The shape which the docker part of the app takes will also be determening
in which kind of fashion the docker setup has to be made.

Making a webless image could be easier in a sence, as there's no porting to be done.
But then how do I capture the outputs of the script provided by the user?

On the ohter hand, catching the output from the user.. perhaps I should provide some methods for retrieving inputs and output paths?


What if I just expect users to write their outputs to the output folder?

```
in:
  - file:
    name: somefile
  - parameter:
    name: myparameter

out:
  - file:
    name: output.txt

    
```


## Internal web service vs flat images


### Flat images
Flat images without a web service are basically dead, I also don't really know how I can handle their outputs.
how does my overarching api know which outout is whcih, and must I create a new image with a differnet output directory every time? That seems unreasonable.
Perhaps there's a way to run an image with a differnet storage location?
a flat image would just be like a pipe. Stuff goes in, stuff comes out. No way to tie api calls into it...
If I want to be able to open up peoples scripts to api stuff, (like triggers or other kinds of calls) I'll have to do something else.



### Internal web services
I think there may be more flexibilty in running an internal service.
or at least more future opportunity.
THen again, how would I se tit up to route trafic from the main api into the container api? 



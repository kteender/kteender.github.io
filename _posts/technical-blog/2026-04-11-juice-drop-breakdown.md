---
title: "KTCG.ART | Pipeline for an Animated Music Video"
shortname: "Animation Pipeline for a Music Video"
date: "2026-04-11"
tags: 
  - "maya"
  - "python"
  - "animation"
cover-image: "/img/2026-04-11-juice-drop-breakdown/cover-image.jpg"
cover-big: "/img/2026-04-11-juice-drop-breakdown/cover-big.jpg"
show-date: T
type: blog
featured: T
uri: "/2025/04/11/juice-drop-breakdown.html"
description: Pipeline breakdown for an animated music video
permalink: juice-drop-breakdown
show-message: T
message: Do you think computers are magic? Don't miss my cybernetic sideshow!!
---
In this post, I will provide a general overview of my animation pipeline. This post uses production materials from <a href="cg-projects#juice-drop">*Juice Drop*</a>, a music video I recently animated. I used this same pipeline on <a href="cg-projects#sewer-issue">*Sewer Issue*</a>, my short last year. Watch the below video to see how I put together the opening 10 seconds of *Juice Drop*, and read the post for additional information!

<!--break-->

<div style="padding:56.25% 0 0 0;position:relative;" id="reels">
    <iframe src="https://www.youtube.com/embed/47k9z3wbGbk?si=jByiH3Zft4LPmfYo" style="position:absolute;top:0;left:0;width:100%;height:100%;" 
    frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
    </iframe>
</div>

The major pipeline phases you see in the video are Storyboards, Previs, Animation, and Polish. I go into more depth below about additional steps.

<div class='captioned-image'>
    <img alt="a storyboard" src='img/2026-04-11-juice-drop-breakdown/intro_breakdown_thumbnail.jpg' style='max-width:max-content;'>
</div>

**Storyboards**: I do not always storyboard animated sequences, but *Juice Drop* was a perfect candidate for storyboards.

<div class='captioned-image'>
    <img alt="a storyboard" src='img/2026-04-11-juice-drop-breakdown/storyboards01.jpg' style='max-width:max-content;'>
    <p>I board on colored paper to help me experiment. There ended up being 126 boards for 63 beats.</p>
</div>

**Capture Script**: I make an initial cut out of the boards, then I determinine the required motions. It is advantageous to have as few setups as possible, so I determine which beats can be captured together. 

<div class='captioned-image'>
    <img alt="capture script" src='img/2026-04-11-juice-drop-breakdown/motionScript.jpg' style='max-width:600px'>
    <p>An excerpt from my capture script.</p>
</div>

<!--break-->

**Slates**: The slate key is as follows: SetupNumber_characterName_RollNumber. This slate will follow the motion around in the filename, clip names, etc. I perform all motions myself. I wear a Rokoko Smartsuit Pro II, Smartgloves, and Headrig (Headrig not pictured).

<div class='captioned-image'>
    <img alt="slating" src='img/2026-04-11-juice-drop-breakdown/slate.jpg' style='max-width:600px'>
    <p>In this example, the slate is S2_customer_R3. </p>
</div>

**Previs**: I run my the output from my capture shoot through my Gesture Drawing plugin, which is a custom Autodesk Maya Python plugin for doing 2.5D motion capture. I wrote the plugin. I refer to the low-res, stick figure gestures as 'motion dailies.' I then do a previs pass, where I edit together the motion dailies based on the cut I created using the boards. 

<div class='captioned-image'>
    <img alt="previs" src='img/2026-04-11-juice-drop-breakdown/previs01.jpg' style='max-width:800px'>
    <p>I reused a storyboard to block in a foreground element. </p>
</div>

I organize my Premiere Pro timeline such that there is a unique track for each character's motion dailies clips, then export <a href="https://en.wikipedia.org/wiki/Edit_decision_list">EDLs</a> for each character.

**Background and Prop Drawing**: One of the most frequent comments I hear about my animation is appreciation for the hand-drawn props and backgrounds. It really makes me happy that viewers value the visibility of the human hand. I sell all my production drawings, so if you like them, head over to the <a href="/shop#art">Story Box Store</a>!

<div class='captioned-image'>
    <img alt="drawing" src='img/2026-04-11-juice-drop-breakdown/drawing.jpg' style='max-width:800px'>
    <p>Using colored India ink and watercolor paper to draw the 'No!' button. </p>
</div>

**Animation**: I print the EDLs from the Previs step so I can annotate them easily. The ranges in the EDL serve as my 'motion selections', and are the guide for the ranges that I need to clean up. 

<div class='captioned-image'>
    <img alt="edls" src='img/2026-04-11-juice-drop-breakdown/edls.jpg' style='max-width:800px'>
    <p>Annotated EDLs at the end of Animation</p>
</div>

Animation depends on the requirements of each shot, but can include:
- Updating the Gesture to a nicer version
- Adding the character's hands (I don't bother with hands for the motion dailies)
- Attaching the character's face (I box-model the faces seperately)
- Running a script I wrote to drive the ARKit blendshapes on the modeled face using the blendshapes on the captured face
- Motion cleanup and sweetening
- Prop animation

<div class='captioned-image'>
    <img alt="animation" src='img/2026-04-11-juice-drop-breakdown/animation.jpg' style='max-width:800px'>
    <p>I often bring video from the shoot in as reference when animating. I set my Maya background to green so it's easy to key out of playblasts.</p>
</div>

**Polish**: I've listed polish as a seperate step, but in reality, Polish and Animation are not clearly seperated. I polish as I go. Polish can include:

- Adding textured overlays to the rendered animation
- Integrating the rendered animation into the background
- Adding video effects to the animation and background to direct the viewers eye
- Using After Effects to generate special effects

..and any other tasks required to make a shot work!

<div class='captioned-image'>
    <img alt="polih" src='img/2026-04-11-juice-drop-breakdown/polish.jpg' style='max-width:800px'>
    <p>I added the glass effect on the sliding door during my polish time.</p>
</div>

**Closing Thoughts**: After completing a project, I take some time to write down my pain points and determine if any were painful enough to warrant code updates. Hindsight often reveals that issues I assumed were technical priorities were, in fact, complete nonissues during production. For this reason, I try to animate as soon as my pipeline code changes are minimum-viable functional.

If you would like a <a href="/rates#animation">price estimate</a> for cartoon animation, I would love to hear from you. I am looking for clients! 
# Slides for Building and sharing machine learning demo applications within life sciences

This folder contains slides for Building and sharing machine learning demo applications within life sciences project.

## How to use

Install [reveal-md](https://github.com/webpro/reveal-md)

To build slides locally: 

```bash
$ reveal-md slides.md -w \
--template assets/revealjs/reveal_template.html \
--css assets/style.css \
--highlight-theme a11y-light
```

To export slides to static page: 

```bash
reveal-md slides.md -w \
--template assets/revealjs/reveal_template.html \
--css assets/style.css \
--highlight-theme a11y-light \
--static-dirs assets/ \
--static slides
```

There is one hiccup static pages though. You need to manually change path to `styles.css` file in `slides/index.html` 

"""
Built-in template registry for ae-automation generate/export commands.

Each template is a dict compatible with TemplateGeneratorMixin.buildTemplate().
"""

BUILTIN_TEMPLATES = {
    "tutorial": {
        "name": "Tutorial Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 10,
        "compositions": [
            {
                "name": "IntroScene",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.2],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "Title",
                        "text": "Tutorial Title",
                        "x": 960,
                        "y": 400,
                        "fontSize": 96,
                    },
                    {
                        "type": "text",
                        "name": "Subtitle",
                        "text": "Step-by-step guide",
                        "x": 960,
                        "y": 600,
                        "fontSize": 48,
                    },
                ],
            },
            {
                "name": "ContentScene",
                "duration": 10,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.95, 0.95, 0.95],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "StepNumber",
                        "text": "Step 1",
                        "x": 960,
                        "y": 200,
                        "fontSize": 64,
                    },
                    {
                        "type": "text",
                        "name": "StepContent",
                        "text": "Description goes here",
                        "x": 960,
                        "y": 540,
                        "fontSize": 42,
                    },
                ],
            },
            {
                "name": "OutroScene",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.2],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "ClosingText",
                        "text": "Thanks for watching!",
                        "x": 960,
                        "y": 540,
                        "fontSize": 72,
                    },
                ],
            },
        ],
    },
    "social-media": {
        "name": "Social Media Template",
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "duration": 15,
        "compositions": [
            {
                "name": "StoryScene",
                "width": 1080,
                "height": 1920,
                "duration": 15,
                "fps": 30,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.2, 0.0, 0.4],
                        "width": 1080,
                        "height": 1920,
                    },
                    {
                        "type": "text",
                        "name": "Headline",
                        "text": "Your Headline Here",
                        "x": 540,
                        "y": 700,
                        "fontSize": 80,
                    },
                    {
                        "type": "text",
                        "name": "CTA",
                        "text": "Swipe Up",
                        "x": 540,
                        "y": 1600,
                        "fontSize": 48,
                    },
                ],
            },
        ],
    },
    "product": {
        "name": "Product Showcase Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 30,
        "compositions": [
            {
                "name": "ProductIntro",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [1.0, 1.0, 1.0],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "BrandName",
                        "text": "Brand Name",
                        "x": 960,
                        "y": 300,
                        "fontSize": 84,
                    },
                    {
                        "type": "text",
                        "name": "ProductName",
                        "text": "Product Name",
                        "x": 960,
                        "y": 540,
                        "fontSize": 64,
                    },
                ],
            },
            {
                "name": "ProductFeatures",
                "duration": 10,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.95, 0.95, 0.95],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "FeatureTitle",
                        "text": "Key Features",
                        "x": 960,
                        "y": 200,
                        "fontSize": 72,
                    },
                    {
                        "type": "text",
                        "name": "FeatureList",
                        "text": "Feature details here",
                        "x": 960,
                        "y": 540,
                        "fontSize": 42,
                    },
                ],
            },
            {
                "name": "ProductCTA",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.0, 0.3, 0.6],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "CTAText",
                        "text": "Get Yours Today",
                        "x": 960,
                        "y": 400,
                        "fontSize": 84,
                    },
                    {
                        "type": "text",
                        "name": "Website",
                        "text": "www.example.com",
                        "x": 960,
                        "y": 600,
                        "fontSize": 48,
                    },
                ],
            },
        ],
    },
    "slideshow": {
        "name": "Slideshow Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 30,
        "compositions": [
            {
                "name": "Slide1",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.15, 0.15, 0.2],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "shape",
                        "name": "ImagePlaceholder",
                        "width": 1200,
                        "height": 675,
                        "color": [0.3, 0.3, 0.35],
                    },
                    {
                        "type": "text",
                        "name": "Caption",
                        "text": "Slide 1 Caption",
                        "x": 960,
                        "y": 900,
                        "fontSize": 48,
                    },
                ],
            },
            {
                "name": "Slide2",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.2, 0.15, 0.15],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "shape",
                        "name": "ImagePlaceholder",
                        "width": 1200,
                        "height": 675,
                        "color": [0.35, 0.3, 0.3],
                    },
                    {
                        "type": "text",
                        "name": "Caption",
                        "text": "Slide 2 Caption",
                        "x": 960,
                        "y": 900,
                        "fontSize": 48,
                    },
                ],
            },
            {
                "name": "Slide3",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.15, 0.2, 0.15],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "shape",
                        "name": "ImagePlaceholder",
                        "width": 1200,
                        "height": 675,
                        "color": [0.3, 0.35, 0.3],
                    },
                    {
                        "type": "text",
                        "name": "Caption",
                        "text": "Slide 3 Caption",
                        "x": 960,
                        "y": 900,
                        "fontSize": 48,
                    },
                ],
            },
        ],
    },
    "event": {
        "name": "Event Promo Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 20,
        "compositions": [
            {
                "name": "EventOpener",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.05, 0.05, 0.1],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "EventName",
                        "text": "Event Name",
                        "x": 960,
                        "y": 400,
                        "fontSize": 96,
                    },
                    {
                        "type": "text",
                        "name": "EventDate",
                        "text": "January 1, 2025",
                        "x": 960,
                        "y": 600,
                        "fontSize": 54,
                    },
                ],
            },
            {
                "name": "EventDetails",
                "duration": 10,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.05, 0.15],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "DetailTitle",
                        "text": "Event Details",
                        "x": 960,
                        "y": 200,
                        "fontSize": 72,
                    },
                    {
                        "type": "text",
                        "name": "Location",
                        "text": "Venue Name, City",
                        "x": 960,
                        "y": 500,
                        "fontSize": 48,
                    },
                    {
                        "type": "text",
                        "name": "Description",
                        "text": "Event description here",
                        "x": 960,
                        "y": 700,
                        "fontSize": 36,
                    },
                ],
            },
            {
                "name": "EventCTA",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.6, 0.0, 0.2],
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "CTAText",
                        "text": "Get Your Tickets Now",
                        "x": 960,
                        "y": 400,
                        "fontSize": 84,
                    },
                    {
                        "type": "text",
                        "name": "TicketURL",
                        "text": "tickets.example.com",
                        "x": 960,
                        "y": 600,
                        "fontSize": 48,
                    },
                ],
            },
        ],
    },
}


def get_template(name):
    """Get a built-in template by name. Returns None if not found."""
    return BUILTIN_TEMPLATES.get(name)


def list_templates():
    """Return a list of (name, description) tuples for all built-in templates."""
    return [(name, cfg["name"]) for name, cfg in BUILTIN_TEMPLATES.items()]

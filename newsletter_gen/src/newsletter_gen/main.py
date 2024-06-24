#!/usr/bin/env python
from newslettercrew import NewsletterGenCrew
import os

def load_html_template():
    with open("src/newsletter_gen/config/newsletter_template.html", "r") as file:
        html_template = file.read()
    return html_template


def run():  
    inputs = {
        "topic": input("Enter the topic: "),
        "html_template": load_html_template(),
    }
    NewsletterGenCrew().crew().kickoff(inputs=inputs)

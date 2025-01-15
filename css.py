block_css = """
#notice_markdown {
    font-size: 104%
}
#notice_markdown th {
    display: none;
}
#notice_markdown td {
    padding-top: 6px;
    padding-bottom: 6px;
}
#leaderboard_markdown {
    font-size: 104%
}
#leaderboard_markdown td {
    padding-top: 6px;
    padding-bottom: 6px;
}
#leaderboard_dataframe td {
    line-height: 0.1em;
}
"""

block_css += """
#mainblock {
    width: 90%;  /* Takes up 90% of the container or viewport width */
    max-width: 1200px;  /* Adjust to your preference for the largest screens */
    margin: 0 auto;  /* Centers the block */
    padding: 10px;
}

/* For larger screens */
@media only screen and (min-width: 768px) {
    #mainblock {
        width: 75%;
    }
}

/* For even larger screens, like desktops */
@media only screen and (min-width: 1200px) {
    #mainblock {
        width: 75%;
    }
}

#tableblock {
    width: 90%;  /* Takes up 90% of the container or viewport width */
    margin: 0 auto;  /* Centers the block */
    padding: 10px;
}
"""

block_css += """
/* If you want the main content to have a slight background to ensure readability,
you can add this style */
#mainblock {
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */
    border-radius: 2%; /* Gives a rounded edge; optional */
    /* other styles for #mainblock remain unchanged */
}

footer {
    visibility: hidden
}

"""

block_css += """
gradio-app > div.gradio-container:first-child {
    /* Path to your image; adjust based on your directory structure */
    background-image: url('https://www.accenture.com/content/dam/accenture/final/images/icons/symbol/Acc_GT_Dimensional_RGB.svg');
    background-size: cover; /* Makes sure the image covers the entire viewport */
    background-repeat: no-repeat; /* Prevents image tiling */
    background-attachment: fixed; /* Keeps the background image fixed during scrolling */
    background-position: center center; /* Centers the image in the viewport */

    /* Adds a semi-transparent black overlay to make the image slightly faded.
    This will make text more readable and give a slightly muted look to the image. */
    background-color: rgba(255, 255, 255, 0.8);
    background-blend-mode: overlay;
}
"""

block_css += """
/* Define a base height for both the button and label. */
#btn, #lbl {
    height: 40px;   /* This sets a fixed height. Adjust as needed. */
    line-height: 40px; /* To vertically center the text */
    display: inline-block; /* To keep them on the same line */
    vertical-align: top;  /* To align them to the top */
}

#lbl {
display: contents;
}

/* Style the button */
#btn {
    background-color: #007BFF; /* A basic blue color; adjust to your needs */
    color: white; 
    border: none;
    border-radius: 4px;  /* Rounded corners */
    padding: 0 15px; /* Padding on left and right. Adjust for button size */
    cursor: pointer;
    transition: background-color 0.3s ease; /* Smooth transition for hover effect */
}

#btn:hover {
    background-color: #0056b3; /* A darker blue for hover; adjust to your needs */
}

/* For responsive designs, adjust styles based on screen sizes using media queries */
@media only screen and (max-width: 600px) {
    /* For screens smaller than 600px */
    #btn, #lbl {
        /* Adjust styles as needed for smaller screens */
        height: 30px;
        line-height: 30px;
    }
}

#lbl div.output-class {
    /* styles go here */
    padding: 2px;
    font-size: large;
}

#doc .label-wrap span:first-of-type {
    font-size: larger; 
    color: #b806f8;
}
#llm .label-wrap span:first-of-type {
    font-size: larger; 
    color: #b806f8;
}
#par .label-wrap span:first-of-type {
    font-size: larger; 
    color: #b806f8;
}
.filebox {
    height:100px;
}
"""

logo_url = "https://www.accenture.com/content/dam/accenture/final/images/icons/symbol/Acc_GT_Dimensional_RGB.svg"
notice_markdown = f"""
# <div style="display: flex; align-items: center; justify-content:center; margin:auto;"><img src="{logo_url}" style="height: 1em; margin-right: 0.5em;" alt="Accenture Logo"/> <p style="text-align: center; font-family: 'Helvetica Neue', Arial, sans-serif;"><span style="color:#b806f8;font-weight: bold;letter-spacing: 1.5px;">Accenture</span> <span style="color:#707070; font-size: 24px;"></span></p></div>
### <p style="text-align: center; color:#b8068f;"> Software Development Life Cycle Assistant <br></p>
"""
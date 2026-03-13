from textwrap import dedent
import urllib.parse

def on_page_markdown(markdown, page, config, files):
    src_uri = getattr(page.file, "src_uri", "") if getattr(page, "file", None) else ""
    if not src_uri.startswith("blog/posts/"):
        return markdown
    
    page_url = urllib.parse.quote(config.site_url + page.url, safe=":/")
    page_title = urllib.parse.quote(page.title + "\n")

    return markdown + dedent(f"""
        <style>
            .floating-share-btn {{
                position: fixed;
                right: 16px;
                top: 55%;
                transform: translateY(-50%);
                z-index: 1000;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 10px 14px;
                background-color: #0077b5;
                color: #fff;
                text-decoration: none;
                border-radius: 999px;
                font-size: 18px;
                font-weight: 600;
                line-height: 1;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}

            .floating-share-btn:hover {{
                filter: brightness(1.05);
            }}

            @media (max-width: 1000px) {{
                .floating-share-btn {{
                    right: 10px;
                    top: auto;
                    bottom: 18px;
                    transform: none;
                    font-size: 16px;
                    padding: 8px 12px;
                }}
            }}
        </style>
        <a class="floating-share-btn"
             href="https://www.linkedin.com/shareArticle?mini=true&url={page_url}&title={page_title}"
             target="_blank"
             rel="noopener noreferrer">
            Share :material-linkedin:
        </a>
        """)
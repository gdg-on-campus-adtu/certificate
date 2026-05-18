# WARNING: Standard LSPs will not work with this file. Open this as a marimo notebook instead.

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import re
    import yagmail
    import polars as pl
    from pathlib import Path
    from PIL import Image, ImageDraw, ImageFont

    return Image, ImageDraw, ImageFont, Path, os, pl, re, yagmail


@app.cell
def _(pl):
    """
    Prepare data
    """

    df = pl.read_excel("assets/record.xlsx").select(["Full Name", "Email Address"])
    df
    return (df,)


@app.cell
def _(Image, ImageDraw, ImageFont, Path, df, re):
    """
    Prepare certificates
    """

    dry_run_certificate = True

    certificate_dir = Path("certificates")
    certificate_dir.mkdir(exist_ok=True)
    template_path = "assets/certificate.png"

    font_path = "assets/font.ttf"
    font = ImageFont.truetype(font_path, 62)

    for idx, row in enumerate(df.iter_rows(named=True)):
        full_name = row["Full Name"].strip()
        certificate_path = (
            certificate_dir
            / f"{re.sub(r'[^\w\s-]', '', full_name).replace(' ', '_')}.png"
        )

        if not dry_run_certificate:
            template = Image.open(template_path)
            draw = ImageDraw.Draw(template)

            bbox = draw.textbbox((0, 0), full_name, font=font)
            text_width = bbox[2] - bbox[0]

            template_width, template_height = template.size
            x_position = int(template_width * 0.06)
            y_position = int(template_height * 0.36)

            draw.text((x_position, y_position), full_name, fill="#1A2533", font=font)
            template.save(certificate_path)

        print(f"{idx + 1}. Written {certificate_path}")
    return (certificate_dir,)


@app.cell
def _(certificate_dir, df, os, re, yagmail):
    """
    Send emails
    """

    dry_run_email = True

    yag = yagmail.SMTP(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_APP_PASSWORD"))

    for idx_two, row_two in enumerate(df.iter_rows(named=True)):
        full_name_two = row_two["Full Name"].strip()
        email = row_two["Email Address"].strip()
        certificate_path_two = (
            certificate_dir
            / f"{re.sub(r'[^\w\s-]', '', full_name_two).replace(' ', '_')}.png"
        )
        contents = f"""Hello {full_name_two}! Here is your <message>"""

        if not dry_run_email:
            yag.send(
                to=email,
                subject="A nice ol' <subject>",
                contents=contents,
                attachments=str(certificate_path_two),
            )

        print(
            f"{idx_two + 1}. Sent {certificate_path_two} to {email}. Good job {full_name_two}!"
        )
    return


if __name__ == "__main__":
    app.run()

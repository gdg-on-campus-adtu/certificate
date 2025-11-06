import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import re
    import yagmail
    import polars as pl
    from dotenv import load_dotenv
    from pathlib import Path
    from PIL import Image, ImageDraw, ImageFont

    load_dotenv()
    return Image, ImageDraw, ImageFont, Path, os, pl, re, yagmail


@app.cell
def _(pl):
    """
    Prepare data
    """

    df = (
        pl.read_csv("assets/attendance.csv")
        .filter(pl.col("Checkin Date (UTC)").is_not_null())
        .select(["First Name", "Last Name", "Email"])
        .with_columns(
            [
                pl.col("First Name").str.to_titlecase().alias("First Name"),
                pl.col("Last Name").str.to_titlecase().alias("Last Name"),
            ]
        )
    )
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

    font_path = "assets/font.otf"
    font = ImageFont.truetype(font_path, 80)

    for idx, row in enumerate(df.iter_rows(named=True)):
        full_name = f"{row['First Name']} {row['Last Name']}"

        if not dry_run_certificate:
            template = Image.open(template_path)
            draw = ImageDraw.Draw(template)

            bbox = draw.textbbox((0, 0), full_name, font=font)
            text_width = bbox[2] - bbox[0]

            template_width, template_height = template.size
            x_position = (template_width - text_width) // 2
            y_position = template_height // 2 - 10

            draw.text((x_position, y_position), full_name, fill="black", font=font)

        certificate_path = (
            certificate_dir
            / f"{re.sub(r'[^\w\s-]', '', full_name).replace(' ', '_')}.png"
        )

        if not dry_run_certificate:
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
        full_name_two = f"{row_two['First Name']} {row_two['Last Name']}"
        email = row_two["Email"].strip()
        certificate_path_two = (
            certificate_dir
            / f"{re.sub(r'[^\w\s-]', '', full_name_two).replace(' ', '_')}.png"
        )
        contents = "<message>"

        if not dry_run_email:
            yag.send(
                to=email,
                subject="<subject>",
                contents=contents,
                attachments=str(certificate_path_two),
            )

        print(
            f"{idx_two + 1}. Sent {certificate_path_two} to {email}. Good job {row_two['First Name']}!"
        )
    return


if __name__ == "__main__":
    app.run()

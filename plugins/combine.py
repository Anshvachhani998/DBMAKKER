from pyrogram import Client, filters
import os
import re
import asyncio
from database.db import db

# =============================
# Config
# =============================
COMBINED_FILE = "combined_track_ids.txt"
DOWNLOAD_DIR = "downloads"

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# =============================
# Helper function
# =============================
def safe_filename(name: str) -> str:
    """Remove unsafe filesystem characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)


# =============================
# 1. Auto combine track IDs when a .txt file is sent
# =============================
@Client.on_message(filters.document & filters.private)
async def auto_combine_track_ids(client, message):
    if not message.document.file_name.endswith(".txt"):
        return

    # Safe path
    safe_name = safe_filename(message.document.file_name)
    file_path = os.path.join(DOWNLOAD_DIR, safe_name)

    try:
        file_path = await message.download(file_path)
    except Exception as e:
        return await message.reply(f"❌ Download failed:\n`{e}`")

    added_ids = 0
    try:
        with open(file_path, "r", encoding="utf-8") as incoming_file:
            incoming_ids = [line.strip() for line in incoming_file if line.strip()]

        # Create combined file if not exists
        if not os.path.exists(COMBINED_FILE):
            open(COMBINED_FILE, "w", encoding="utf-8").close()

        # Append all incoming IDs
        with open(COMBINED_FILE, "a", encoding="utf-8") as combined_file:
            for track_id in incoming_ids:
                combined_file.write(track_id + "\n")
                added_ids += 1

        await message.reply(f"✅ `{added_ids}` track IDs added (including duplicates).")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")


# =============================
# 2. /clear command to wipe the combined file
# =============================
@Client.on_message(filters.command("clear") & filters.private)
async def clear_combined_file(client, message):
    if os.path.exists(COMBINED_FILE):
        open(COMBINED_FILE, "w", encoding="utf-8").close()
        await message.reply("🧹 Combined track list cleared.")
    else:
        await message.reply("⚠️ No file to clear.")


# =============================
# 3. /getfile command to send the combined file
# =============================
@Client.on_message(filters.command("getfile") & filters.private)
async def send_combined_file(client, message):
    if os.path.exists(COMBINED_FILE):
        await message.reply_document(COMBINED_FILE, caption="📄 Combined Track IDs")
    else:
        await message.reply("⚠️ No combined file found yet.")


# =============================
# 4. /checkall command to check tracks in DB (duplicates removed)
# =============================
@Client.on_message(filters.command("checkall") & filters.private & filters.reply)
async def check_tracks_in_db(client, message):
    if not message.reply_to_message.document:
        return await message.reply("❗ Please reply to a `.txt` file containing track IDs (one per line).")

    status_msg = await message.reply("📥 Downloading file and fetching DB data...")

    safe_name = safe_filename(message.reply_to_message.document.file_name)
    file_path = os.path.join(DOWNLOAD_DIR, safe_name)

    try:
        file_path = await message.reply_to_message.download(file_path)
    except Exception as e:
        return await status_msg.edit(f"❌ Download failed:\n`{e}`")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]
        total_tracks_before = len(raw_lines)  # Before removing duplicates
        lines = list(dict.fromkeys(raw_lines))  # Remove duplicates, preserve order
        total_tracks_after = len(lines)  # After removing duplicates
        duplicates_removed = total_tracks_before - total_tracks_after

    # Step 1: Load existing track IDs from DB
    existing_tracks = set()
    async for doc in db.dump_col.find({}, {"track_id": 1, "_id": 0}):
        existing_tracks.add(doc["track_id"])

    # Step 2: Compare with DB
    new_tracks = []
    already_in_db = 0

    for idx, track_id in enumerate(lines, 1):
        if track_id not in existing_tracks:
            new_tracks.append(track_id)
        else:
            already_in_db += 1

        # Progress update every 10k
        if idx % 10000 == 0 or idx == total_tracks_after:
            try:
                await status_msg.edit(
                    f"🔎 Checking tracks...\n"
                    f"Total IDs in file: {total_tracks_before}\n"
                    f"Unique IDs after duplicates removed: {total_tracks_after}\n"
                    f"Duplicates removed: {duplicates_removed}\n"
                    f"Checked so far: {idx}\n"
                    f"Already in DB: {already_in_db}\n"
                    f"New Tracks: {len(new_tracks)}"
                )
            except Exception:
                pass

    # Step 3: If no new tracks
    if not new_tracks:
        return await status_msg.edit(
            f"✅ Done! All tracks already exist in DB.\n"
            f"Duplicates removed: {duplicates_removed}"
        )

    # Step 4: Split into batches and send
    batch_size = 10000000  # adjust as needed
    batches = [new_tracks[i:i + batch_size] for i in range(0, len(new_tracks), batch_size)]

    for i, batch in enumerate(batches, 1):
        filename = f"new_tracks_part_{i}.txt"
        batch_file_path = os.path.join(DOWNLOAD_DIR, filename)

        with open(batch_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(batch))

        await client.send_document(
            chat_id=message.chat.id,
            document=batch_file_path,
            caption=f"✅ New Tracks Batch {i}/{len(batches)} - {len(batch)} tracks"
        )
        await asyncio.sleep(2)

    await status_msg.edit(
        f"✅ Completed!\n"
        f"Total IDs in file: {total_tracks_before}\n"
        f"Unique IDs after duplicates removed: {total_tracks_after}\n"
        f"Duplicates removed: {duplicates_removed}\n"
        f"Already in DB: {already_in_db}\n"
        f"New tracks files sent: {len(batches)}"
    )

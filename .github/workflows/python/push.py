#!/usr/bin/env python3

import os
import re
import subprocess

repo_path = os.environ['GITHUB_WORKSPACE']

# Regex to match text like [[Test File | return to test file]]

bear_title_pattern = re.compile(r'^\#\s+(.+)')
custom_link_pattern = re.compile(r'\[\[\s*([^\|\]]+)\s*\|\s*([^\]]+)\s*\]\]')
link_pattern = re.compile(r'\[\[\s*([^\]]+)\s*\]\]')


# Function to replace custom link format with Markdown links
def replace_custom_links(content):

	def replacement(match):
		file_name = match.group(1).strip()  # Extract the file name
		link_text = match.group(2).strip()  # Extract the link text
		file_name.replace(" ", "_")
		return f"[{link_text}]({file_name}.md)"  # Convert to Markdown format

	return custom_link_pattern.sub(replacement, content)


# Function to replace custom link format with Markdown links
def replace_standard_links(content):

	def replacement(match):
		file_name = match.group(1).strip()  # Extract the file name
		file_name_formatted = file_name.replace(" ", "_")
		return f"[{file_name}]({file_name_formatted}.md)"  # Convert to Markdown format

	return link_pattern.sub(replacement, content)


def replace_bear_titles(content):

	def replacement(match):
		file_name = match.group(1)  # Extract the file name
		file_name_formatted = file_name.replace(" ", "_")
		return f"[{file_name}]({file_name_formatted}.md)"  # Convert to Markdown format

	return bear_title_pattern.sub(replacement, content)


def get_all_files():
	"""Get a list of files in repo"""
	result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
	return result.stdout.splitlines()


def is_markdown_file(file_path):
	"""Check if a file is a markdown file (not binary)"""
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			file.read()
			if file_path.endswith('.md'):
				return True
	except (UnicodeDecodeError, FileNotFoundError):
		return False


def process_file(file_path):
	"""Read, modify, and update the file content"""
	with open(f"{repo_path}/{file_path}", 'r', encoding='utf-8') as file:
		content = file.read()

	# Replace custom links with Markdown links
	updated_content = replace_custom_links(content)
	updated_content = replace_standard_links(updated_content)
	updated_content = replace_bear_titles(updated_content)
	
	# Replace soace with _ in filenames
	file_path_formatted = file_path.replace(" ","_")
	os.rename(f"{repo_path}/{file_path_formatted}",)
	if updated_content != content:
		# Write the updated content back to the file
		with open(file_path, 'w', encoding='utf-8') as file:
			file.write(updated_content)
  
	# Add the modified file back to the staging area
	subprocess.run(['git', 'add', file_path])


def main():
	# Get all staged files
	all_files = get_all_files()

	# Process each staged file
	for file_path in all_files:
		if is_markdown_file(file_path):  # Only process markdown files
			process_file(file_path)


if __name__ == '__main__':
	main()

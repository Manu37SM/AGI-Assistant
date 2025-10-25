import os, json, re

def summarize_session(timeline):
    # Simple rule-based summarizer: look for keywords in OCR + transcripts
    events = timeline.get('events', [])
    transcripts = timeline.get('transcript', [])
    ocr_texts = ' '.join([e.get('ocr_text','') for e in events])
    speech_text = ' '.join([t.get('text','') for t in transcripts])

    summary_parts = []
    suggestions = []

    if 'excel' in ocr_texts.lower() or 'excel' in speech_text.lower():
        summary_parts.append('User interacted with Excel (detected via OCR or speech).')
        suggestions.append({
            'id':'auto_excel_open_save',
            'title':'Open Excel and Save File',
            'steps_summary':['Open Excel','Save file (Ctrl+S)'],
            'confidence':0.6,
            'frequency':1
        })

    if 'notepad' in ocr_texts.lower() or 'notepad' in speech_text.lower():
        summary_parts.append('User used Notepad.')
        suggestions.append({
            'id':'auto_notepad',
            'title':'Open Notepad and Save',
            'steps_summary':['Open Notepad','Type text','Save file'],
            'confidence':0.5,
            'frequency':1
        })

    if not summary_parts:
        # generic fallback
        # try to extract short verbs from speech
        verbs = []
        for t in transcripts:
            txt = t.get('text','')
            if txt:
                verbs.extend(re.findall(r"\b(open|save|close|type|copy|paste|download)\b", txt.lower()))
        if verbs:
            summary_parts.append('Detected actions from speech: ' + ', '.join(verbs))

    summary = ' '.join(summary_parts) if summary_parts else 'No prominent app-specific actions detected.'
    return summary, suggestions

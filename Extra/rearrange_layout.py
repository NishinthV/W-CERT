import re

file_path = 'w-cert-frontend/src/pages/Dashboard/IncidentDetail.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(\s*\{/\* Main Content \*/\}.*?)(\s*\{/\* Escalation Modal \*/\})'
match = re.search(pattern, content, re.DOTALL)
grid_content = match.group(1)
escalation_modal = match.group(2)

markers = [
    '{/* Description Card */}',
    '{/* Evidence Card */}',
    '{/* IPC Legal Sections */}',
    '{/* Evidence Gaps */}',
    '{/* Similar Past Cases (RAG) */}',
    '{/* Chain of Custody */}',
    '{/* AI Threat Score Card */}',
    '{/* Verification Analysis */}'
]

blocks = {}

for marker in markers:
    start_idx = grid_content.find(marker)
    if start_idx == -1: continue
    
    # We will find the first <div or <Link after the marker, OR if it has a wrapping logic like `incident.ipc_sections?.length > 0 && (` we need to find the start of that logic.
    # To be safe, we just capture from the marker down to the next marker or end of grid
    end_idx = len(grid_content)
    for other in markers:
        if other == marker: continue
        idx = grid_content.find(other, start_idx + len(marker))
        if idx != -1 and idx < end_idx:
            end_idx = idx
            
    block_text = grid_content[start_idx:end_idx]
    
    # We must trim off closing </div> tags that actually belong to the column wrapper.
    # Since we know our blocks, let's just strip trailing whitespace and the last '</div>' if it belongs to the wrapper.
    # Wait, the easiest way to avoid stripping the wrong div is just to use the exact component strings.
    # Let's count divs in block_text to ensure it's balanced.
    
    blocks[marker] = block_text.strip()

# wait, if we just use string finding, the last block before a column closing </div> might include that closing </div>!
# Let's clean the blocks manually.
# In `IncidentDetail.jsx`, the columns were:
# lg:col-span-2: Description Card, Evidence Card, then closing </div>
# Then floating: IPC Legal Sections, Evidence Gaps, Similar Past Cases, Chain of Custody
# Then space-y-6 (Right Column): AI Threat Score Card, Verification Analysis, then closing </div>

# We can find the exact blocks by manually looking at the text.
def extract_balanced(text, marker):
    start = text.find(marker)
    if start == -1: return ""
    
    # Find the first opening brace or tag
    i = start + len(marker)
    while i < len(text) and text[i] not in '<{':
        i += 1
        
    stack = 0
    in_jsx_expr = False
    
    for j in range(i, len(text)):
        if text[j:j+4] == '<div' or text[j:j+5] == '<Link':
            stack += 1
        elif text[j:j+5] == '</div' or text[j:j+6] == '</Link':
            stack -= 1
            if stack == 0 and not in_jsx_expr:
                end_tag = text.find('>', j)
                # wait, what if it's `{incident.ipc... && ( <div...></div> )}` ?
                # Then the JSX expression is wrapped in { ... }
                # Let's just use the fact that each of our blocks either starts with <div className="cyber-card" or is wrapped in {incident... && ( <div className="cyber-card" ) }
                pass

# Simpler logic:
def get_block(start_marker, end_string):
    start = grid_content.find(start_marker)
    if start == -1: return ""
    end = grid_content.find(end_string, start) + len(end_string)
    return grid_content[start:end]

blocks['{/* Description Card */}'] = get_block('{/* Description Card */}', '</p>\n                    </div>')
blocks['{/* Evidence Card */}'] = get_block('{/* Evidence Card */}', '</div>\n                        )}\n                    </div>')

blocks['{/* IPC Legal Sections */}'] = get_block('{/* IPC Legal Sections */}', '</p>\n                        </div>\n                    )}')
blocks['{/* Evidence Gaps */}'] = get_block('{/* Evidence Gaps */}', '</div>\n                        </div>\n                    )}')
blocks['{/* Similar Past Cases (RAG) */}'] = get_block('{/* Similar Past Cases (RAG) */}', '</p>\n                        </div>\n                    )}')
blocks['{/* Chain of Custody */}'] = get_block('{/* Chain of Custody */}', 'AES-256 GCM.\n                        </p>\n                    </div>')

blocks['{/* AI Threat Score Card */}'] = get_block('{/* AI Threat Score Card */}', '</span>\n                        </div>\n\n                        {/* Integrity Hash */}\n                        <div className="pt-4 border-t border-white/5 mt-4">\n                            <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-2">Integrity Hash</div>\n                            <div className="font-mono text-[10px] text-gray-600 break-all bg-black/40 p-2 rounded">\n                                {incident.content_hash}\n                            </div>\n                        </div>\n                    </div>')
blocks['{/* Verification Analysis */}'] = get_block('{/* Verification Analysis */}', '</div>\n                                </div>\n                            )}\n                        </div>\n                    </div>')


new_grid = f"""
                {{/* Main Content */}}
                <div className="lg:col-span-2 space-y-6">
                    {blocks['{/* Description Card */}']}
                    
                    {blocks['{/* Evidence Card */}']}
                    
                    {blocks['{/* Verification Analysis */}']}
                    
                    {blocks['{/* IPC Legal Sections */}']}
                    
                    {blocks['{/* Similar Past Cases (RAG) */}']}
                </div>

                {{/* Sidebar Analysis */}}
                <div className="space-y-6">
                    {blocks['{/* AI Threat Score Card */}']}
                    
                    {blocks['{/* Evidence Gaps */}']}
                    
                    {blocks['{/* Chain of Custody */}']}
                </div>
            </div>
"""

new_content = content[:match.start(1)] + new_grid + content[match.start(2):]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done reorganizing layout!")

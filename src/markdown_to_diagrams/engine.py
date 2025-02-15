"""Module for parsing markdown files and extracting relevant sections for diagram generation"""

from markdown_to_diagrams.llm import LLMClient
from markdown_to_diagrams.persistence import PersistenceClient
from markdown_to_diagrams.log_util import LogUtil
from markdown_to_diagrams.config import Config
import glob, os

class DiagramEngine:
    """Parser for extracting diagram-related content from markdown files"""

    def __init__(self, file_name):
        """Initialize the markdown parser"""
        self.file_path = f"process/{file_name}.md"
        self.file_name = f"{file_name}"
        self.folder_path = f"process"
        self._persistence_client = PersistenceClient()
        self._logger = LogUtil.get_logger()
        self._llm_client = LLMClient()
        pass

    def process(self):
        """Parse the markdown file and extract sections for diagram generation

        Args:
            file_path (str): Path to the markdown file

        Returns:
            list: List of sections that need diagram generation
        """
        # TODO: Implement markdown parsing logic
        pass
    
    def process_sequence_diagram(self):
        """Parse the markdown file and extract sections for diagram generation
        Args:
            file_path (str): Path to the markdown file
        Returns:
            list: List of sections that need diagram generation
        """
        
        doc = self._persistence_client.load_file(self.file_path)

        messages = [
                {"role": "user", "content": f'''
Analyze the content of the following document and determine whether the document contains the following information:

Requirements:

- Determine whether the entire document contains content suitable for visualization as a [sequence diagram]
- The judgment criteria should be strict; only confirmed interaction process and relationship information should be expressed in a [sequence diagram]
- Repeat the above process until all information suitable for sequence diagram visualization is found
- For each piece of information, summarize and generate a Mermaid sequence diagram
- Output in JSON list format for me

```json
{{ sequence_diagrams:
[
  {{summarized_caption:"",
  mermaid_Sequence_diagram:""}}
]
}}
```

- If the document does not contain any information suitable for being displayed in a sequence diagram, then return an empty list.

```json
{{ sequence_diagrams:
[]
}}
```

---

Documentation：

```
{doc}
```

        '''}
            ]
        
        try:
            response = self._llm_client.chat_completion(messages, model=Config.SMART_MODEL, response_format='json')
            print(response)
            file_path = f'{self.folder_path}/{self.file_name}/sequence_diagrams.json'
            self._persistence_client.save_json(data=response, file_path=file_path)
            self._logger.info(f"Successfully generated sequence diagrams to {file_path}")
            return response
        except Exception as e:
            error_msg = f"Failed to generated sequence diagrams: {str(e)}"
            self._logger.error(error_msg)
            raise


    def process_pie_chart(self):
        """Parse the markdown file and extract sections for diagram generation
        Args:
            file_path (str): Path to the markdown file
        Returns:
            list: List of sections that need diagram generation
        """
        
        doc = self._persistence_client.load_file(self.file_path)

        messages = [
                {"role": "user", "content": f'''
Analyze the content of the following document and determine whether the document contains the following information:

Requirements:

- Determine whether the entire document contains content suitable for visualization as a [pie chart]
- The judgment criteria should be strict; only confirmed information about proportions, possession rates, and similar content should be expressed in a [pie chart].
- Repeat the above process until all information suitable for pie chart visualization is found
- For each piece of information, summarize and generate a Mermaid pie chart
    - value only numberic, no % mark
Pie Chart Example:

```mermaid
pie title Customer Retention
    "Project Phoenix": 45
    "StyleNow": 55
    "FashionForward": 52
```

- Output in JSON list format for me

```json
{{ pie_charts:
[
  {{summarized_caption:"",
  mermaid_pie_chart:""}}
]
}}
```

- If the document does not contain any information suitable for being displayed in a pie chart, then return an empty list.

```json
{{ pie_charts:
[]
}}
```

---

Documentation：

```
{doc}
```

        '''}
            ]
        
        try:
            response = self._llm_client.chat_completion(messages, model=Config.SMART_MODEL, response_format='json')
            print(response)
            file_path = f'{self.folder_path}/{self.file_name}/pie_charts.json'
            self._persistence_client.save_json(data=response, file_path=file_path)
            self._logger.info(f"Successfully generated sequence diagrams to {file_path}")
            return response
        except Exception as e:
            error_msg = f"Failed to generated sequence diagrams: {str(e)}"
            self._logger.error(error_msg)
            raise

    def process_gantt_chart(self):
        """Parse the markdown file and extract sections for diagram generation
        Args:
            file_path (str): Path to the markdown file
        Returns:
            list: List of sections that need diagram generation
        """
        
        doc = self._persistence_client.load_file(self.file_path)

        messages = [
                {"role": "user", "content": f'''
Analyze the content of the following document and determine whether the document contains the following information:

Requirements:

- Determine whether the entire document contains content suitable for visualization as a [gantt chart]
- The judgment criteria should be strict; only confirmed information about timeline and phases order/relation should be expressed in a [gantt chart].
- Repeat the above process until all information suitable for gantt chart visualization is found
- For each piece of information, summarize and generate a Mermaid gantt chart
Example Gantt:
```
gantt
    dateFormat  YYYY-MM-DD
    title       Adding GANTT diagram functionality to mermaid
    section A section
    Completed_task:done,    taskcode, 2014-01-06,2014-01-08
```
- Output in JSON list format for me

```json
{{ gantt_charts:
[
  {{summarized_caption:"",
  mermaid_gantt_chart:""}}
]
}}
```


- If the document does not contain any information suitable for being displayed in a gantt chart, then return an empty list.

```json
{{ gantt_charts:
[]
}}
```

---

Documentation：

```
{doc}
```

        '''}
            ]
        
        try:
            response = self._llm_client.chat_completion(messages, model=Config.SMART_MODEL, response_format='json')
            print(response)
            file_path = f'{self.folder_path}/{self.file_name}/gantt_charts.json'
            self._persistence_client.save_json(data=response, file_path=file_path)
            self._logger.info(f"Successfully generated sequence diagrams to {file_path}")
            return response
        except Exception as e:
            error_msg = f"Failed to generated sequence diagrams: {str(e)}"
            self._logger.error(error_msg)
            raise

    def process_final_markdown(self):
        """Process all generated JSON files and create a final markdown with diagrams
        Returns:
            str: Path to the generated markdown file
        """
        # Read all JSON files from the folder
        folder_path = f'{self.folder_path}/{self.file_name}'
        merged_data = []
        
        json_files = glob.glob(os.path.join(folder_path, '*.json'))
        for json_file in json_files:
            try:
                data = self._persistence_client.load_json(os.path.relpath(json_file))
                # Use filename without extension as the diagram type
                merged_data.append(data)
            except Exception as e:
                self._logger.warning(f"Could not load {file_path}: {str(e)}")
                continue
            except Exception as e:
                self._logger.warning(f"Could not list JSON files in {folder_path}: {str(e)}")
                merged_data = []
                 
        
        doc = self._persistence_client.load_file(self.file_path)
        # Prepare prompt for markdown generation
        messages = [
            {"role": "user", "content": f'''
Please help me process the text.

- You will be provided with a complete [document] and relevant [Diagrams]
- Please insert the corresponding Mermaid diagrams into the appropriate positions in the original document based on the titles of the diagrams
- Apart from this, keep the original document content word for word, without modifying, omitting, or changing the format
- Only insert the Mermaid Diagram text into the original Markdown-formatted article
- Output the full final Markdown document to me

Diagrams to be inserted:
{merged_data}

Original Documentation:
{doc}
'''}
        ]

        try:
            response = self._llm_client.chat_completion(messages, model=Config.SMART_MODEL, response_format='markdown')
            output_path = f'{self.folder_path}/{self.file_name}_output.md'
            self._persistence_client.save_file(content=response, file_path=output_path)
            self._logger.info(f"Successfully generated final markdown file at {output_path}")
            return output_path
        except Exception as e:
            error_msg = f"Failed to generate final markdown: {str(e)}"
            self._logger.error(error_msg)
            raise


if __name__ == "__main__":
    engine = DiagramEngine('fake_demo1')
    engine.process_sequence_diagram()
    engine.process_pie_chart()
    engine.process_gantt_chart()
    engine.process_final_markdown()
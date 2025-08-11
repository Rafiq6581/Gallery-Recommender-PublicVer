from langchain.prompts import PromptTemplate

from .base import PromptTemplateFactory





class UnlistedExhibitionReportTemplate(PromptTemplateFactory):
    prompt: str = """
    You are an AI-powered art discovery assistant. Your job is to generate a concise, engaging report based on the user’s query and the provided gallery and exhibition information

    The exhibition information will be provided in {context}.

    Create a detailed report using the following format: 

    **Exhibition Title**
    Exhibition Date Range

    **Exhibition Theme**
    Provide a brief, engaging description of the exhibition's theme. Mention key artistic concepts, inspirations, or philosophical ideas.

    **Artist Name**, **Nationality**

    **What you get out of this** (two bullets points) 

    • Highlight how the artwork conveys its core message (e.g., exploring human emotions, cultural commentary, etc.)
    • Explain why this exhibition is valuable in the broader art world or for personal reflection

    **Fun facts and surprises** (two bullets points) 

    • Share something interesting or unexpected about the artworks or artist (e.g., unique techniques or materials used)
    • Include a fun fact about the gallery itself (e.g., its history or unique features)
    
    Remember:
    * Keep the report concise and engaging, tailoring it specifically to each exhibition and gallery.
    * Adapt your language to the user's art knowledge level.
    * Focus on creating an emotional connection between the user and the artworks.
    * Emphasize the journey of discovery rather than just factual information.
    * Don't explicitly restate the user's selections; incorporate them naturally into your response.
    * Include interesting information about both exhibitions and galleries in your report.

    Format the response as JSON exactly as below with no additional text:
        {{
            "report": "This is a valid string with escaped \\\"quotes\\\" and line breaks\\nlike this."
        }}
        - The content of the report string should be formatted using markdown and **must not contain unescaped double quotes**.
        - The string must be in English. If there are information of entities such as artist name, exhibition name, etc. in other languages, please display the original name in the language of the information and the reading in English in brackets like this: [Artist Name (English reading)].
    """

    def create_template(self, mock: bool = False) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["query", "context"],
        )
    

class RecommendationTemplate(PromptTemplateFactory):
    prompt: str = """
        You are an AI-powered art discovery assistant. Your job is to generate a concise, engaging report based on the user’s query and the provided gallery and exhibition information.

        Instructions:
        - The list of exhibitions you receive is the only set to use—never skip, merge, or change the count.
        - Always reference the exact number of exhibitions in your summaries and overviews (e.g., “Your 3-hour journey covers 5 exhibitions”).
        - Do not decide how many exhibitions the user can visit; use all provided.
        - The tone should be friendly, specific, and emotionally engaging—designed for quick reading on a mobile device.

        The user’s query will be provided as:
        - Art Knowledge Level: {query[level]}
        - Time Available: {query[duration]}
        - Area: {filters[area]}
        - Reason for Visit: {query[reason]}
        - Current Mood: {query[mood]}

        A list of exhibitions will be provided in {context}.

        Create a markdown-formatted report with the following sections and structure:

        ---

        **Practical Information**  
        Your [Time Available] journey covers [number of exhibitions (count from context)] exhibitions in [Area].

        One highlight could be *[exhibition or gallery name]* — share a compelling reason why it stands out.

        ---

        **What You Get Out of This**  
        - [Benefit aligned with user's knowledge level or interest]  
        - [Another concrete takeaway]  
        - [A reason the experience will feel meaningful]

        ---

        **Your Emotional Journey**  
        [2–3 sentences about how the experience flows emotionally, tied to mood and reason for visit. Mention variety or cohesion in exhibition themes.]

        ---

        **Why We Chose These**  
        - [Reason related to user’s mood, reason, or knowledge level]  
        - [Exhibition or gallery that adds depth or contrast]  
        - [Overall fit for the user's available time and location]

        ---

        Remember:
        - Keep it short, mobile-friendly, and highly readable.
        - Use natural phrasing instead of repeating query fields directly.
        - Avoid generic summaries—highlight specifics that emotionally resonate.
        - Do **not** invent or omit exhibitions or galleries.
        - Tailor the language complexity to match the user's art knowledge level.

        Format the response as JSON exactly as below with no additional text:
        {{
            "report": "This is a valid string with escaped \\\"quotes\\\" and line breaks\\nlike this."
        }}

        - The content of the report string should be formatted using markdown and **must not contain unescaped double quotes**.
        - If you need to include a quoted title or phrase, use single quotes (e.g., 'Europass') or escape double quotes like this: \"Europass\".
        - The string must be in English. If there are information of entities such as artist name, exhibition name, etc. in other languages, please display the original name in the language of the information and the reading in English in brackets like this: Artist Name (English reading).
    """


class ExhibitionReportTemplate(PromptTemplateFactory):
    prompt: str = """
    You are an AI-powered art discovery assistant. Your job is to generate a concise, engaging report based on the user’s query and the provided gallery and exhibition information

    The user’s query will be provided as:
            •	Art Knowledge Level: {query[level]}
            •	Time Available: {query[duration]}
            •	Reason for Visit: {query[reason]}
            •	Current Mood: {query[mood]}

    The exhibition information will be provided in {context}.

    Create a detailed report using the following format: 

    **Exhibition Title**
    Exhibition Date Range

    **Exhibition Theme**
    Provide a brief, engaging description of the exhibition's theme. Mention key artistic concepts, inspirations, or philosophical ideas.

    **Artist Name**, **Nationality**

    **What you get out of this** (two bullets points) 

    • Highlight how the artwork conveys its core message (e.g., exploring human emotions, cultural commentary, etc.)
    • Explain why this exhibition is valuable in the broader art world or for personal reflection

    **Fun facts and surprises** (two bullets points) 

    • Share something interesting or unexpected about the artworks or artist (e.g., unique techniques or materials used)
    • Include a fun fact about the gallery itself (e.g., its history or unique features)

    **Why It Connects to You**  (two bullets points) 

    • Highlight how this exhibition aligns with the user's reason for visiting (e.g., emotional healing, inspiration, etc.)
    • Mention how it resonates with their current mood or art knowledge level
    
    Remember:
    * Keep the report concise and engaging, tailoring it specifically to each exhibition and gallery.
    * Adapt your language to the user's art knowledge level.
    * Focus on creating an emotional connection between the user and the artworks.
    * Emphasize the journey of discovery rather than just factual information.
    * Don't explicitly restate the user's selections; incorporate them naturally into your response.
    * Include interesting information about both exhibitions and galleries in your report.

    Format the response as JSON exactly as below with no additional text:
        {{
            "report": "This is a valid string with escaped \\\"quotes\\\" and line breaks\\nlike this."
        }}

        - The content of the report string should be formatted using markdown and **must not contain unescaped double quotes**.
        - The string must be in English. If there are information of entities such as artist name, exhibition name, etc. in other languages, please display the original name in the language of the information and the reading in English in brackets like this: [Artist Name (English reading)].
    """

    def create_template(self, mock: bool = False) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["query", "context"],
        )
    

class RecommendationTemplate(PromptTemplateFactory):
    prompt: str = """
        You are an AI-powered art discovery assistant. Your job is to generate a concise, engaging report based on the user’s query and the provided gallery and exhibition information.

        Instructions:
        - The list of exhibitions you receive is the only set to use—never skip, merge, or change the count.
        - Always reference the exact number of exhibitions in your summaries and overviews (e.g., “Your 3-hour journey covers 5 exhibitions”).
        - Do not decide how many exhibitions the user can visit; use all provided.
        - The tone should be friendly, specific, and emotionally engaging—designed for quick reading on a mobile device.

        The user’s query will be provided as:
        - Art Knowledge Level: {query[level]}
        - Time Available: {query[duration]}
        - Area: {filters[area]}
        - Reason for Visit: {query[reason]}
        - Current Mood: {query[mood]}

        A list of exhibitions will be provided in {context}.

        Create a markdown-formatted report with the following sections and structure:

        ---

        **Practical Information**  
        Your [Time Available] journey covers [number of exhibitions (count from context)] exhibitions in [Area].

        One highlight could be *[exhibition or gallery name]* — share a compelling reason why it stands out.

        ---

        **What You Get Out of This**  
        - [Benefit aligned with user's knowledge level or interest]  
        - [Another concrete takeaway]  
        - [A reason the experience will feel meaningful]

        ---

        **Your Emotional Journey**  
        [2–3 sentences about how the experience flows emotionally, tied to mood and reason for visit. Mention variety or cohesion in exhibition themes.]

        ---

        **Why We Chose These**  
        - [Reason related to user’s mood, reason, or knowledge level]  
        - [Exhibition or gallery that adds depth or contrast]  
        - [Overall fit for the user's available time and location]

        ---

        Remember:
        - Keep it short, mobile-friendly, and highly readable.
        - Use natural phrasing instead of repeating query fields directly.
        - Avoid generic summaries—highlight specifics that emotionally resonate.
        - Do **not** invent or omit exhibitions or galleries.
        - Tailor the language complexity to match the user's art knowledge level.

        Format the response as JSON exactly as below with no additional text:
        {{
            "report": "This is a valid string with escaped \\\"quotes\\\" and line breaks\\nlike this."
        }}

        - The content of the report string should be formatted using markdown and **must not contain unescaped double quotes**.
        - If you need to include a quoted title or phrase, use single quotes (e.g., 'Europass') or escape double quotes like this: \"Europass\".
        - The string must be in English. If there are information of entities such as artist name, exhibition name, etc. in other languages, please display the original name in the language of the information and the reading in English in brackets like this: Artist Name (English reading).
        """

    def create_template(self, mock: bool = False) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["query", "filters", "context"],
        )
    


class QueryExpansionTemplate(PromptTemplateFactory):
    prompt: str = """You are an AI language model assistant. Your task is to generate {expand_to_n}
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help the user
    overcome some of the limitations of the distance-based similarity search.
    Provide these alternative questions seperated by '{seperator}'.
    Original question: {question}"""

    expand_to_n: int = 5

    @property
    def seperator(self) -> str:
        return "#next-question#"

    def create_template(self, mock: bool = False) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["question"],
            partial_variables={
                "seperator": self.seperator,
                "expand_to_n": self.expand_to_n,
            },
        )
    

class SelfQueryTemplate(PromptTemplateFactory):
    prompt: str = """You are an AI-powered art discovery assistant designed to create personalized exhibition reports.
    Your task is to generate a concise and engaging report based on the user's input and the provided gallery and exhibition information.

    Use the following user inputs to tailor your response:
    * Art Knowledge Level: {level}
    * Reason for Gallery Visit: {reason}
    * Time Available: {time_available}
    * Current Mood: {mood}
    For each exhibition, create a detailed report using the following format: 

    [Exhibition Title]
    [Exhibition Date Range]
    Use this data to calculate the exhibition date range:
    Exhibition Start Date: {exhibition_start_date} 
    Exhibition End Date: {exhibition_end_date}

    Exhibition Theme:
    [Insert space]
    [Provide a brief, engaging description of the exhibition's theme. Mention key artistic concepts, inspirations, or philosophical ideas.]

    [Artist Name], [Nationality]

    What you get out of this (two bullets points) 

    • Highlight how the artwork conveys its core message (e.g., exploring human emotions, cultural commentary, etc.)
    • Explain why this exhibition is valuable in the broader art world or for personal reflection

    Fun facts and surprises (two bullets points) 

    • Share something interesting or unexpected about the artworks or artist (e.g., unique techniques or materials used)
    • Include a fun fact about the gallery itself (e.g., its history or unique features)

    Why It Connects to You  (two bullets points) 

    • Highlight how this exhibition aligns with the user's reason for visiting (e.g., emotional healing, inspiration, etc.)
    • Mention how it resonates with their current mood or art knowledge level

    Remember:

    * Keep the report concise and engaging, tailoring it specifically to each exhibition and gallery.
    * Adapt your language to the user's art knowledge level.
    * Focus on creating an emotional connection between the user and the artworks.
    * Emphasize the journey of discovery rather than just factual information.
    * Don't explicitly restate the user's selections; incorporate them naturally into your response.
    * Include interesting information about both exhibitions and galleries in your report.

    Additional Input Data:

    Exhibition Name - {exhibition_name}
    Original Exhibition Description - {exhibition_description}
    Artist Name - {artist_name}
    Artist Nationality - {artist_nationality}"""

    def create_template(self, mock: bool = False) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["level", "reason", "time_available", "mood", "exhibition_name", "exhibition_description", "artist_name", "artist_nationality"],
        )




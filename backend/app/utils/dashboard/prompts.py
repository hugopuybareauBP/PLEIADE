# backend/app/utils/dashboard/prompts.py

from langchain.prompts import ChatPromptTemplate

target_reader_prompt_template = ChatPromptTemplate.from_template(
    """
    Rate the likelihood (0–100%) that this synopsis appeals to the following reader segments:\n
    - Young Adult (13–17)\n
    - New Adult (18–25)\n"
    - Adult (26–45)\n"
    - Mature (46+)\n\n"
    Respond in the exact format, one per line:\n"
    Young Adult (13–17): XX%\n"
    New Adult (18–25): XX%\n"
    Adult (26–45): XX%\n"
    Mature (46+): XX%\n\n"
    Synopsis: {text}"
    """
)

genre_prompt_template = ChatPromptTemplate.from_template(
    """
    Distribute exactly 100% across the following genres to reflect how likely the book we analyze belongs to each one.\n
    Use the definitions below to guide your classification.\n

    IMPORTANT FORMAT RULES:\n
    - The total must equal exactly 100%.\n
    - DO NOT USE SCORES THAT END IN 0 OR 5.\n
    - Only use percentages ending in 1, 2, 3, 4, 6, 7, 8, or 9. This ensures stylistic consistency.\n

    Example (valid format):\n
    Narrative Fiction (Novel or Short Story): 7%\n
    Poetry: 3%\n
    Drama: 18%\n
    Essay: 9%\n
    ...\n

    Genre definitions:\n
    - Novel or Short Story: Fictional prose, the book is short, focusing on plot and character development.\n
    - Poetry: Literary work focused on the expression of feelings and ideas through rhythm, style, and metaphorical language.\n
    - Drama: A work intended for performance on stage, focusing on dialogue and action.\n
    - Essay: A short nonfiction text presenting an argument or personal reflection on a specific topic.\n
    - Autobiography / Memoir: A personal narrative written by the subject, recounting their own life or experiences.\n
    - Biography: A factual, third-person account of someone's life written by someone else.\n
    - Crime / Detective Fiction: Stories centered on solving a crime or mystery, often involving a detective or investigator.\n
    - Science Fiction: Speculative fiction involving futuristic science, technology, space, or other scientific elements.\n
    - Fantasy: Fiction set in imaginary worlds, often involving magic, mythical creatures, or supernatural events.\n
    - Historical Fiction: Fictional stories set in the past, often featuring real historical events or figures.\n\n

    Respond in this exact format, one line per genre:\n
    Narrative Fiction (Novel or Short Story): XX%\n
    Poetry: XX%\n
    Drama: XX%\n
    Essay: XX%\n
    Autobiography / Memoir: XX%\n
    Biography: XX%\n
    Crime / Detective Fiction: XX%\n
    Science Fiction: XX%\n
    Fantasy: XX%\n
    Historical Fiction: XX%\n\n

    Here is the chapter one:\n
    {text}
    """
)

emblematic_authors_by_genre = {
    "Novel or Short Story": [
        "Jane Austen", "Leo Tolstoy", "Honoré de Balzac", "Franz Kafka", "Virginia Woolf",
        "F. Scott Fitzgerald", "Ernest Hemingway", "Gabriel García Márquez", "Haruki Murakami", "Toni Morrison",
        "George Orwell", "Albert Camus", "William Faulkner", "Chinua Achebe", "Clarice Lispector",
        "Raymond Carver", "Alice Munro", "Italo Calvino", "J. M. Coetzee", "Margaret Atwood"
    ],
    "Poetry": [
        "Homer", "Dante Alighieri", "William Shakespeare", "Emily Dickinson", "Charles Baudelaire",
        "Arthur Rimbaud", "Walt Whitman", "Federico García Lorca", "Sylvia Plath", "Pablo Neruda",
        "Langston Hughes", "Anna Akhmatova", "W. B. Yeats", "Rainer Maria Rilke", "Rabindranath Tagore",
        "Aimé Césaire", "Paul Celan", "Wislawa Szymborska", "Nâzım Hikmet", "Louise Glück"
    ],
    "Drama": [
        "Sophocles", "William Shakespeare", "Molière", "Henrik Ibsen", "Anton Chekhov",
        "Tennessee Williams", "Samuel Beckett", "Jean Racine", "Bertolt Brecht", "Jean-Paul Sartre",
        "Eugene O’Neill", "Harold Pinter", "Yasmina Reza", "Caryl Churchill", "Eugène Ionesco",
        "Lorraine Hansberry", "Arthur Miller", "Wole Soyinka", "Sarah Kane", "Tom Stoppard"
    ],
    "Essay": [
        "Michel de Montaigne", "Jean-Jacques Rousseau", "Virginia Woolf", "Simone de Beauvoir", "Roland Barthes",
        "George Orwell", "Susan Sontag", "James Baldwin", "Hannah Arendt", "Umberto Eco",
        "Frantz Fanon", "Edward Said", "Claude Lévi-Strauss", "Alain Finkielkraut", "Rebecca Solnit",
        "Mona Chollet", "Baptiste Morizot", "Annie Le Brun", "Didier Eribon", "Ta-Nehisi Coates"
    ],
    "Autobiography / Memoir": [
        "Jean-Jacques Rousseau", "Saint Augustine", "Benjamin Franklin", "Marguerite Yourcenar", "Simone de Beauvoir",
        "Nelson Mandela", "Maya Angelou", "Annie Ernaux", "Patrick Modiano", "Giacomo Casanova",
        "André Gide", "Romain Gary", "Marguerite Duras", "Hervé Guibert", "Leïla Slimani",
        "Édouard Louis", "Jean-Paul Sartre", "Marcel Pagnol", "Karl Ove Knausgård", "Michelle Obama"
    ],
    "Biography": [
        "Plutarch", "James Boswell", "Stefan Zweig", "Jean Lacouture", "Claire Tomalin",
        "Walter Isaacson", "Elizabeth Gaskell", "André Maurois", "Richard Ellmann", "Peter Ackroyd",
        "David McCullough", "Robert Caro", "Emmanuel Carrère", "Jean Echenoz", "Jean d’Ormesson",
        "Marguerite Yourcenar", "Pierre Assouline", "Doris Kearns Goodwin", "Brenda Maddox", "Victoria Glendinning"
    ],
    "Crime / Detective Fiction": [
        "Arthur Conan Doyle", "Agatha Christie", "Raymond Chandler", "Dashiell Hammett", "Georges Simenon",
        "Émile Gaboriau", "Wilkie Collins", "Patricia Highsmith", "P. D. James", "Ian Rankin",
        "Michael Connelly", "Henning Mankell", "Jo Nesbø", "Stieg Larsson", "Tana French",
        "Walter Mosley", "Dorothy L. Sayers", "Karin Fossum", "Ruth Rendell", "Andrea Camilleri"
    ],
    "Science Fiction": [
        "Jules Verne", "H. G. Wells", "Mary Shelley", "Isaac Asimov", "Arthur C. Clarke",
        "Ray Bradbury", "Philip K. Dick", "Robert A. Heinlein", "Ursula K. Le Guin", "Frank Herbert",
        "William Gibson", "Octavia E. Butler", "Stanisław Lem", "Kim Stanley Robinson", "Aldous Huxley",
        "Karel Čapek", "Liu Cixin", "Neal Stephenson", "Connie Willis", "John Scalzi"
    ],
    "Fantasy": [
        "J. R. R. Tolkien", "C. S. Lewis", "George R. R. Martin", "Ursula K. Le Guin", "Terry Pratchett",
        "Brandon Sanderson", "J. K. Rowling", "Robin Hobb", "Philip Pullman", "Patrick Rothfuss",
        "Andrzej Sapkowski", "Robert Jordan", "Naomi Novik", "Guy Gavriel Kay", "Lev Grossman",
        "Susanna Clarke", "Neil Gaiman", "Anne Rice", "Sarah J. Maas", "Tamora Pierce"
    ],
    "Historical Fiction": [
        "Sir Walter Scott", "Alexandre Dumas", "Hilary Mantel", "Robert Graves", "Philippa Gregory",
        "Patrick O’Brian", "Bernard Cornwell", "Mary Renault", "Ken Follett", "Umberto Eco",
        "James Clavell", "Colleen McCullough", "Sharon Kay Penman", "Jean-Christophe Rufin", "Arthur Golden",
        "Eleanor Hibbert", "Taylor Caldwell", "Steven Pressfield", "Conn Iggulden", "Marguerite Yourcenar"
    ]
}

style_dna_prompt_template = ChatPromptTemplate.from_template(
    """
    You are a literary style analyst. You are given a literary text and its genre.\n
    Your task is to estimate which authors have most influenced the style of this text. Use only the list of authors provided for the genre "{genre}".\n
    For each author of the list, assign a percentage score (total must equal 100). Then explain, in 1 to 3 sentences, why that author's style is reflected in the text (consider sentence structure, tone, narration, themes, atmosphere, etc.).\n

    IMPORTANT FORMAT RULES:\n
    - The total must equal exactly 100%.\n
    - Only use percentages ending in 0, 1, 2, 3, 4, 6, 7, 8, or 9. This ensures stylistic consistency.\n

    Return the result in a **JSON array** with the following format:\n
    [
    {{
        "author": "Author Name",
        "score": 25,
        "justification": "Brief explanation of the stylistic influence."
    }},
    ...
    ]

    List of emblematic authors for the genre "{genre}":
    {authors_list}

    Text to analyze:
    <<<
    {text}
    >>>
    """
)
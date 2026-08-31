import os
from io import StringIO
from contextlib import redirect_stdout

def output_parser(messages, filename):
    filename = f"output/{filename}"
    os.makedirs(os.path.dirname(filename), exist_ok= True)

    cnt = 1

    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                cnt = (
                    content.count("Query") + 1
                )
        except Exception as e:
            print(e)
    
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write("=" * 80 + "\n")
            f.write(f"Query {cnt}\n")
            f.write("=" * 80 + "\n\n")

            for message in messages:
                buffer = StringIO()

                with redirect_stdout(buffer):
                    message.pretty_print()

                f.write("\n")
                f.write(buffer.getvalue())
                f.write("\n")
            
            f.write("=" * 80 + "\n")
    
    except Exception as e:
        print(e)
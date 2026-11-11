demo/        deployment demo (Gradio, Flair 2, opened through an SSH tunnel)
  A  question 7 (comparison): correct "yes" with only 1 of 2 gold passages read; same at 64 and 128 vectors
  B  question 8 (two-hop, paternal grandfather of Felicity Tree): perfect retrieval, answer stops at the first hop
  C  own one-hop question (father of Felicity Tree): right person, garbled first name
  D  seed-43 budget head: learned split [32,16,8,8] differs from uniform, same answer
appendix/    execution evidence: output of "python3 show_step_a3.py <step>" (steps 1-10; a/b = two screens of one step)
comparison/  comparison with a standard text RAG: output of "python3 code/compare_rag_systems.py" on the server and the
             comparison demo (demo_app_compare.py)

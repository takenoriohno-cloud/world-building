# -*- coding: utf-8 -*-
import re

with open("world/magic/spells/movement.md", "r", encoding="utf-8") as f:
    text = f.read()

# Fix brackets and naming cleanups
text = text.replace("《瞬間矢よけ旧名：射撃武器屈折》", "《瞬間矢よけ》（旧名：射撃武器屈折）")
text = text.replace("《荷重軽減旧名：軽荷》", "《荷重軽減》（旧名：軽荷）")
text = text.replace("《錠前大師旧名：鍵開け》", "《錠前大師》（旧名：鍵開け）")
text = text.replace("《飛行術旧名：飛行*》", "《飛行術*》（旧名：飛行*）")
text = text.replace("《水泳術旧名：水泳》", "《水泳術》（旧名：水泳）")

text = text.replace("《見当識並》", "《見当識》（並）")
text = text.replace("《工芸補助並》", "《工芸補助》（並）")
text = text.replace("《クッション並》", "《クッション》（並）")
text = text.replace("《疾走並》", "《疾走》（並）")
text = text.replace("《開扉並》", "《開扉》（並）")
text = text.replace("《沈ませ並》", "《沈ませ》（並）")

with open("world/magic/spells/movement.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Text polish complete.")

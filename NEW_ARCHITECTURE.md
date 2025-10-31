# Proposal for Refactored Architecure of Statica

## Preface

I was looking through the source code, during a week-end and in my opinion it is rather "messy" (professionally speaking it suffers from monolithic design, poor separation of code) and could benefit from "modularization". Current code base might be functional (I really didn't test the accuracy of it) but clearly it lacks proper error handling.

Therefore I gave a little thought and came up with a better architecure to this, although might not be perfect it will give a starting point 
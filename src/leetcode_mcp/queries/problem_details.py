query = """query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {            
            questionId
            questionFrontendId
            title
            content
            likes
            dislikes
            stats
            similarQuestions
            categoryTitle
            hints
            topicTags { name }
            companyTags { name }
            difficulty
            isPaidOnly
            codeSnippets {
                lang
                langSlug
                code
            }
            solution { canSeeDetail content }
            hasSolution 
            hasVideoSolution
        }
    }"""

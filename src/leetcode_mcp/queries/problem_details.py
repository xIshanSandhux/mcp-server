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


#
#     query questionDetail($titleSlug: String!) {
#   languageList {
#     id
#     name
#   }
#   submittableLanguageList {
#     id
#     name
#     verboseName
#     isCompiledLang
#   }
#   statusList {
#     id
#     name
#   }
#   questionDiscussionTopic(questionSlug: $titleSlug) {
#     id
#     commentCount
#     topLevelCommentCount
#   }
#   ugcArticleOfficialSolutionArticle(questionSlug: $titleSlug) {
#     uuid
#     chargeType
#     canSee
#     hasVideoArticle
#   }
#   question(titleSlug: $titleSlug) {
#     title
#     titleSlug
#     questionId
#     questionFrontendId
#     questionTitle
#     translatedTitle
#     content
#     translatedContent
#     categoryTitle
#     difficulty
#     stats
#     companyTagStatsV2
#     topicTags {
#       name
#       slug
#       translatedName
#     }
#     positionLevelTags {
#       name
#       nameTranslated
#       slug
#     }
#     similarQuestionList {
#       difficulty
#       titleSlug
#       title
#       translatedTitle
#       isPaidOnly
#     }
#     mysqlSchemas
#     dataSchemas
#     frontendPreviews
#     likes
#     dislikes
#     isPaidOnly
#     status
#     canSeeQuestion
#     enableTestMode
#     metaData
#     enableRunCode
#     enableSubmit
#     enableDebugger
#     envInfo
#     isLiked
#     nextChallenges {
#       difficulty
#       title
#       titleSlug
#       questionFrontendId
#     }
#     libraryUrl
#     adminUrl
#     hints
#     codeSnippets {
#       code
#       lang
#       langSlug
#     }
#     exampleTestcaseList
#     hasFrontendPreview
#     featuredContests {
#       titleSlug
#       title
#     }
#     aiJudgingAvailable
#   }
# }
#

$(document).ready(function() {
    var candidatesList = [];

    $(".each-candidate").each(function() {
        var gradeTag = $(this).attr("data-grade-tags");
        var userId = $(this).attr("id");
        var currentTown = $(this).attr("data-current-town");
        var gradeScore = $(this).attr("data-grade-score");
        var topStudent = $(this).attr("data-top-student");

        gradeTag = gradeTag.replace("[", "").replace("]", "").replace(/u'/g, "").replace(/'/g, "");
        var allTags = gradeTag.split(", ");

        allTags = $.map(allTags, function(n,i){return n.toLowerCase();}); // change tags (skills) to lowercase

        var currentTownList = currentTown.split(", ");

        var candidate = {userId: userId, tags: allTags, score: gradeScore, topStudent: topStudent};

        candidatesList.push(candidate);

        //alert(candidatesList);
    });

    $("#filter-top-students").click(function(e) {
        e.preventDefault();
        var candidate;
        for(candidate in candidatesList) {
            if(candidatesList[candidate].topStudent == 0) {
                $("#"+candidatesList[candidate].userId).hide();
            } else {
                $("#"+candidatesList[candidate].userId).show();
            }
        }
    });

    $("#filter-show-all").click(function(e) {
        e.preventDefault();
        var candidate;
        for(candidate in candidatesList) {
            $("#"+candidatesList[candidate].userId).show();
        }
    });

    $("#searchButton").click(function(e) {
        e.preventDefault();
        var skills = $("#skillSearch").val();

        var skillsList = skills.split(",");

        skillsList = $.map(skillsList, function(n,i){return n.toLowerCase();}); // change skills to lowercase

        for(s in skillsList) {
            if(skillsList[s].charAt(0) == " ") {
                skillsList[s] = skillsList[s].substring(1);
            }
        }

        var candidate;
        for(candidate in candidatesList) {
            var canId = $("#"+candidatesList[candidate].userId);
            var user = candidatesList[candidate];

            canId.show();

            for(ss in skillsList) {
                if(jQuery.inArray(skillsList[ss], user.tags) === -1) {
                    canId.hide();
                }
            }
        }
    });
});


$(document).ready(function() {
    var candidatesList = [];

    // only unique values when joining two arrays. Usage: var array3 = arrayUnique(array1.concat(array2));
    function arrayUnique(array) {
        var a = array.concat();
        for(var i=0; i<a.length; ++i) {
            for(var j=i+1; j<a.length; ++j) {
                if(a[i] === a[j])
                    a.splice(j--, 1);
            }
        }

        return a;
    };

    // init
    $(".each-candidate").each(function() {
        var gradeTag = $(this).attr("data-grade-tags");
        var otherSkills = $(this).attr("data-other-skills");
        var userId = $(this).attr("id");
        var currentTown = $(this).attr("data-current-town");
        var gradeScore = $(this).attr("data-grade-score");
        var topStudent = $(this).attr("data-top-student");

        // remove python list brackets and unicode u'
        gradeTag = gradeTag.replace("[", "").replace("]", "").replace(/u'/g, "").replace(/'/g, "");
        otherSkills = otherSkills.replace("[", "").replace("]", "").replace(/u'/g, "").replace(/'/g, "");
        var allTags = gradeTag.split(", ");
        var otherSkillsList = otherSkills.split(", ");

        allTags = $.map(allTags, function(n,i){return n.toLowerCase();}); // change tags (skills) to lowercase
        otherSkillsList = $.map(otherSkillsList, function(n,i){return n.toLowerCase();}); // change tags (skills) to lowercase

        var currentTownList = currentTown.split(", ");
        currentTownList = $.map(currentTownList, function(n,i){return n.toLowerCase();}); // change towns to lowercase

        allTags = arrayUnique(allTags.concat(currentTownList));
        allTags = arrayUnique(allTags.concat(otherSkillsList));

        var candidate = {userId: userId, tags: allTags, score: gradeScore, topStudent: topStudent};

        candidatesList.push(candidate);

        //alert(candidatesList);
    });

    // show only top candidates
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

    // Show all candidates
    $("#filter-show-all").click(function(e) {
        e.preventDefault();
        var candidate;
        for(candidate in candidatesList) {
            $("#"+candidatesList[candidate].userId).show();
        }
    });

    // search
    $("#searchButton").click(function(e) {
        e.preventDefault();

        var skills = $("#skillSearch").val();

        // if search input field is empty, show all candidates
        if(!skills) {
            $(".each-candidate").each(function() {
                $(this).show();
            });
            return;
        }

        var skillsList = skills.split(","); // put skills from input into array

        skillsList = $.map(skillsList, function(n,i){return n.toLowerCase();}); // change skills to lowercase

        // remove redundant white spaces
        for(var s in skillsList) {
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


function timeFromSeconds(seconds){
	var secondString = seconds%60;
	if(secondString < 10){
		secondString = "0"+secondString;
	}
	var minutes = parseInt(seconds/60);
	var minuteString = minutes%60;
	if(minuteString < 10){
		minuteString = "0"+minuteString;
	}
	var hours = parseInt(minutes/60);
	var hourString = hours;
	if(hourString < 10){
		hourString = "0"+hourString;
	}
	return {'hours':hourString,'minutes':minuteString,'seconds':secondString};
}

function runTimer(startTime,projectId){
		//seconds = 1;
	timer = setInterval(function() {
		var seconds =  Math.round((new Date - startTime) / 1000);
		//console.log(startTime);
		var timeString = timeFromSeconds(seconds);
		$('.seconds_'+projectId).text(timeString.seconds);
		$('.minutes_'+projectId).text(timeString.minutes);
		$('.hours_'+projectId).text(timeString.hours);
	}, 1000);
} 
function alreadyRunning(projectId,openStart,comment){
	if(openStart != "None"){
		var start = new Date(openStart);
		runTimer(start,projectId);
		$(".panelBox_"+projectId).addClass("activeTimerBox");
		$(".stopBtn_"+projectId).removeAttr("disabled");
		$(".startBtn_"+projectId).attr("disabled","disabled");
		//console.log(comment)
		if(comment == "" || comment == "None"){
			comment = "Insert Comment";
		}
		$(".commentBox_"+projectId).show();
		$(".trackingComment").val(comment);
	}
}
function staticOverallTime(seconds,projectId){
	var timeString = timeFromSeconds(seconds);
	$(".overalTime_"+projectId).text("Overall Time: "+timeString.hours+":"+timeString.minutes);
	$(".overalTimeProjectView_"+projectId).text(timeString.hours+":"+timeString.minutes+":"+timeString.seconds);
}
function lastRecord(seconds,projectId){
	var timeString = timeFromSeconds(seconds);
	$(".lastRecord_"+projectId).text(timeString.hours+":"+timeString.minutes+":"+timeString.seconds);
}
function todayTime(seconds,projectId){
	var timeString = timeFromSeconds(seconds);
	$(".today_"+projectId).text(timeString.hours+":"+timeString.minutes+":"+timeString.seconds);
}
function weekTime(seconds,projectId){
	var timeString = timeFromSeconds(seconds);
	$(".thisWeek_"+projectId).text(timeString.hours+":"+timeString.minutes+":"+timeString.seconds);
}
function monthTime(seconds,projectId){
	var timeString = timeFromSeconds(seconds);
	$(".thisMonth_"+projectId).text(timeString.hours+":"+timeString.minutes+":"+timeString.seconds);
}
function notAccountedTime(seconds,projectId){
	var timeString = timeFromSeconds(seconds);
	$(".notAccountedTime_"+projectId).text(timeString.hours+":"+timeString.minutes+":"+timeString.seconds);
}

// add project
$("#addProject").click(function(){
	var projectName = $(".projectName").val().trim();
	//alert(projectName);
	if(projectName != ""){
		var data = 'projectName=' + projectName + '&viewType={{projects.viewType}}';
        $.ajax({
            url: "/addProject",
            type: "POST",
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            data: data,
            success: function (fn) {
            	window.location.reload(true);
            }
        });
	}
});
function toggleDisplayInput(clickElement,thisId,sendDest){
	var thisText = clickElement.text();
	if(thisText != ""){
		clickElement.removeClass("boldHeadline").html('<input type="text" class="inputField" value="'+thisText+'">');
	}
	$(".inputField").on('keyup',function(){
		var thisText = $(this).val();
	}).on('keypress',function(event){
		if(event.which == 13){
			sendToggleInsert(sendDest,thisId,$(this).val());
			$(this).parent(".toggleDisplayInput").html($(this).val()).addClass("boldHeadline");
		}
	}).on('focusout',function(){
		$(this).parent(".toggleDisplayInput").html(thisText).addClass("boldHeadline");
	}).focus();

}

function sendToggleInsert(dest,id,content){
	var data = 'changeId=' + id + '&changeContent='+encodeURIComponent(content);
        $.ajax({
            url: "/"+dest,
            type: "POST",
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            data: data,
            success: function (fn) {
            	//window.location.reload(true);
            }
        });
	return false;
}
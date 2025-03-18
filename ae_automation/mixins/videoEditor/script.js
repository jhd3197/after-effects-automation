$(document).ready(function() {
    var zoomLevel = 1;
    var maxZoomLevel = 5;
    var minZoomLevel = 0.5;

    function updateZoom() {
        var totalWidth = 0;
        $('.scene').each(function() {
            var duration = $(this).data('duration');
            var startTime = $(this).data('starttime');
            var newWidth = duration * zoomLevel * 10;
            var newLeft = startTime * zoomLevel * 10;
            $(this).css('width', newWidth + 'px');
            $(this).css('left', newLeft + 'px');
            totalWidth = Math.max(totalWidth, newLeft + newWidth);
        });
        $('.timeline-container').css('width', totalWidth + 'px');

        // Check if scrolling is necessary
        if (totalWidth > $('.timeline-container-wrapper').width()) {
            $('.timeline-container-wrapper').css('overflow-x', 'auto');
        } else {
            $('.timeline-container-wrapper').css('overflow-x', 'hidden');
        }

        updateTimer();
    }

    function updateTimer() {
        $('#timer').empty();
        var interval;
        if (zoomLevel <= 1) {
            interval = 15;
        } else if (zoomLevel <= 2) {
            interval = 10;
        } else {
            interval = 5;
        }

        var totalSeconds = 3600;
        var numMarks = totalSeconds / interval;
        for (var i = 0; i <= numMarks; i++) {
            var seconds = i * interval;
            var minutes = Math.floor(seconds / 60);
            var remainingSeconds = seconds % 60;
            var timeText = minutes.toString().padStart(2, '0') + ':' + remainingSeconds.toString().padStart(2, '0') + 's';
            var markPosition = i * interval * zoomLevel * 10;

            var minuteMark = $('<div class="minute-mark"></div>').css('left', markPosition + 'px');
            var minuteLabel = $('<div class="minute-label"></div>').text(timeText).css('left', markPosition + 'px');
            $('#timer').append(minuteMark).append(minuteLabel);
        }
    }

    $('#zoom-in').on('click', function() {
        if (zoomLevel < maxZoomLevel) {
            zoomLevel += 0.1;
            $('#zoom-slider').val(zoomLevel);
            updateZoom();
        }
    });

    $('#zoom-out').on('click', function() {
        if (zoomLevel > minZoomLevel) {
            zoomLevel -= 0.1;
            $('#zoom-slider').val(zoomLevel);
            updateZoom();
        }
    });

    $('#zoom-slider').on('input', function() {
        zoomLevel = $(this).val();
        updateZoom();
    });

    $('.scene').draggable({
        axis: 'x',
        grid: [10, 10],
        start: function(event, ui) {
            $('#drag-line').show();
            $('#drag-time').show();
            $('#timeline-current-position').show();
        },
        drag: function(event, ui) {
            var position = ui.position.left;
            var startTime = position / (zoomLevel * 10);
            var minutes = Math.floor(startTime / 60);
            var seconds = Math.floor(startTime % 60);
            var timeText = minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0') + 's';

            $('#drag-line').css('left', position + 'px');
            $('#drag-time').css('left', position + 'px').text(timeText);
            $('#timeline-current-position').text(timeText);
        },
        stop: function(event, ui) {
            var newStartTime = ui.position.left / (zoomLevel * 10);
            $(this).data('starttime', newStartTime);
            $('#drag-line').hide();
            $('#drag-time').hide();
            $('#timeline-current-position').hide();
            updateData();
        }
    }).resizable({
        handles: 'e, w',
        grid: [10, 10],
        resize: function(event, ui) {
            var newWidth = ui.size.width;
            var startTime = ui.position.left / (zoomLevel * 10);
            var duration = newWidth / (zoomLevel * 10);
            var endTime = startTime + duration;
            var minutes = Math.floor(endTime / 60);
            var seconds = Math.floor(endTime % 60);
            var timeText = minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0') + 's';

            $('#timeline-current-position').text(timeText).show();
        },
        stop: function(event, ui) {
            var newDuration = ui.size.width / (zoomLevel * 10);
            $(this).data('duration', newDuration);
            $('#timeline-current-position').hide();
            updateData();
        }
    });

    $('#project-form').on('submit', function(e) {
        e.preventDefault();
        updateData();
    });

    $('#add-scene').on('click', function() {
        addScene();
    });

    $(document).on('click', '.edit-scene', function() {
        var sceneElement = $(this).closest('.scene');
        editScene(sceneElement);
    });

    $(document).on('click', '.delete-scene', function() {
        var sceneElement = $(this).closest('.scene');
        sceneElement.remove();
        updateData();
    });

    $(document).on('click', '.scene', function() {
        $('.scene').removeClass('highlight');
        $(this).addClass('highlight');
        $('#add-custom-action').show();
    });

    $(document).on('dblclick', '.scene', function() {
        var sceneElement = $(this);
        var startTime = sceneElement.data('starttime');
        var duration = sceneElement.data('duration');

        Swal.fire({
            title: 'Edit Scene',
            html:
                '<p style="margin: 0;">Start Time: </p> <input id="swal-input-start" class="swal2-input" placeholder="Start Time" value="' + startTime + '">' +
                '<p style="margin: 0;margin-top: 15px;">Duration: </p> <input id="swal-input-duration" class="swal2-input" placeholder="Duration" value="' + duration + '">',
            focusConfirm: false,
            preConfirm: () => {
                return {
                    startTime: document.getElementById('swal-input-start').value,
                    duration: document.getElementById('swal-input-duration').value
                };
            }
        }).then((result) => {
            if (result.isConfirmed) {
                var newStartTime = parseFloat(result.value.startTime);
                var newDuration = parseFloat(result.value.duration);

                if (!isNaN(newStartTime) && !isNaN(newDuration)) {
                    sceneElement.data('starttime', newStartTime);
                    sceneElement.data('duration', newDuration);
                    updateZoom();
                    updateData();
                }
            }
        });
    });

    $(document).on('click', '.accordion-header', function() {
        var content = $(this).next('.accordion-content');
        var arrow = $(this).find('.toggle-arrow');
        var track = $(this).closest('.track');
    
        content.slideToggle(200, function() {
            if (content.is(':visible')) {
                track.addClass('expanded');
            } else {
                track.removeClass('expanded');
            }
        });
    
        if (arrow.text() === '▼') {
            arrow.text('▲');
        } else {
            arrow.text('▼');
        }
    });

    $('#add-custom-action').on('click', function() {
        var highlightedScene = $('.scene.highlight');
        if (highlightedScene.length) {
            addCustomAction(highlightedScene);
        }
    });

    function addCustomAction(sceneElement) {
        Swal.fire({
            title: 'Add Custom Action',
            html:
                '<p style="margin: 0;">Change Type: </p> <input id="swal-input-change-type" class="swal2-input" placeholder="Change Type">' +
                '<p style="margin: 0;margin-top: 15px;">Comp Name: </p> <input id="swal-input-comp-name" class="swal2-input" placeholder="Comp Name">' +
                '<p style="margin: 0;margin-top: 15px;">Layer Name: </p> <input id="swal-input-layer-name" class="swal2-input" placeholder="Layer Name">' +
                '<p style="margin: 0;margin-top: 15px;">Property Name: </p> <input id="swal-input-property-name" class="swal2-input" placeholder="Property Name">' +
                '<p style="margin: 0;margin-top: 15px;">Property Type: </p> <input id="swal-input-property-type" class="swal2-input" placeholder="Property Type">' +
                '<p style="margin: 0;margin-top: 15px;">Value: </p> <input id="swal-input-value" class="swal2-input" placeholder="Value">',
            focusConfirm: false,
            preConfirm: () => {
                return {
                    changeType: document.getElementById('swal-input-change-type').value,
                    compName: document.getElementById('swal-input-comp-name').value,
                    layerName: document.getElementById('swal-input-layer-name').value,
                    propertyName: document.getElementById('swal-input-property-name').value,
                    propertyType: document.getElementById('swal-input-property-type').value,
                    value: document.getElementById('swal-input-value').value
                };
            }
        }).then((result) => {
            if (result.isConfirmed) {
                var customActions = sceneElement.data('custom_actions') || [];
                customActions.push(result.value);
                sceneElement.data('custom_actions', customActions);
                updateCustomActions(sceneElement);
                updateData();
            }
        });
    }
    
    $(document).on('click', '.toggle-arrow', function() {
        var sceneElement = $(this).closest('.scene');
        var accordionContent = sceneElement.find('.accordion-content');
        
        if (accordionContent.is(':visible')) {
            accordionContent.slideUp();
            $(this).html('&#9660;');
        } else {
            accordionContent.slideDown();
            $(this).html('&#9650;');
        }

        sceneElement.closest('.track').toggleClass('expanded');
    });

    function updateCustomActions(sceneElement) {
        var customActions = sceneElement.data('custom_actions') || [];
        var customActionsList = sceneElement.find('.custom-actions-list');
        customActionsList.empty();
        customActions.forEach(function(action) {
            customActionsList.append('<li>' +
                'Change Type: ' + action.changeType + '<br>' +
                'Layer Name: ' + action.layerName + '<br>' +
                'Comp Name: ' + action.compName + '<br>' +
                'Layer Index: ' + action.layerIndex +
            '</li>');
        });
    }

    function updateData() {
        var projectForm = $('#project-form').serializeArray();
        var projectData = {};
        $.each(projectForm, function(i, field) {
            projectData[field.name] = field.value;
        });

        var scenes = [];
        $('.scene').each(function() {
            var scene = {
                name: $(this).data('name'),
                duration: $(this).data('duration'),
                startTime: $(this).data('starttime'),
                template_comp: $(this).data('template_comp'),
                reverse: $(this).data('reverse'),
                custom_actions: $(this).data('custom_actions') || []
            };
            scenes.push(scene);
        });

        var data = {
            project: projectData,
            timeline: scenes,
            file_path: projectData.project_file // Adjusted to use projectData.project_file
        };

        $.ajax({
            url: '/update',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                console.log(response.message);
            }
        });
    }

    function addScene() {
        var newScene = {
            name: "New Scene",
            duration: 60,
            startTime: 0,
            template_comp: "",
            reverse: false,
            custom_actions: []
        };
        var sceneElement = $('<div class="scene"></div>')
            .data('name', newScene.name)
            .data('duration', newScene.duration)
            .data('starttime', newScene.startTime)
            .data('template_comp', newScene.template_comp)
            .data('reverse', newScene.reverse)
            .data('custom_actions', newScene.custom_actions)
            .css('width', newScene.duration * zoomLevel * 10 + 'px')
            .css('left', newScene.startTime * zoomLevel * 10 + 'px')
            .append('<div class="scene-info accordion-header"><p>' + newScene.name + '</p></div>')
            .append('<div class="accordion-content"><h3>Custom Actions</h3><div class="custom-actions-list"></div></div>')
            .draggable({
                axis: 'x',
                grid: [10, 10],
                start: function(event, ui) {
                    $('#drag-line').show();
                    $('#drag-time').show();
                },
                drag: function(event, ui) {
                    var position = ui.position.left;
                    var startTime = position / (zoomLevel * 10);
                    var minutes = Math.floor(startTime / 60);
                    var seconds = Math.floor(startTime % 60);
                    var timeText = minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0') + 's';

                    $('#drag-line').css('left', position + 'px');
                    $('#drag-time').css('left', position + 'px').text(timeText);
                    $('#timeline-current-position').text(timeText);
                },
                stop: function(event, ui) {
                    var newStartTime = ui.position.left / (zoomLevel * 10);
                    $(this).data('starttime', newStartTime);
                    $('#drag-line').hide();
                    $('#drag-time').hide();
                    $('#timeline-current-position').text('00:00s');
                    updateData();
                }
            })
            .resizable({
                handles: 'e, w',
                grid: [10, 10],
                stop: function(event, ui) {
                    var newDuration = ui.size.width / (zoomLevel * 10);
                    $(this).data('duration', newDuration);
                    updateData();
                }
            });
        $('.tracks').append('<div class="track">' + sceneElement[0].outerHTML + '</div>');
        updateData();
    }

    function populateResources() {
        var resourcesList = $('#resources-list');
        resourcesList.empty();

        projectData.resources.forEach(function(resource) {
            var resourceItem = $('<div class="resource-item"></div>')
                .text(resource.name + ' (' + resource.type + ')')
                .data('resource', resource);
            resourcesList.append(resourceItem);
        });

        // Handle resource click
        $('.resource-item').on('click', function() {
            var resource = $(this).data('resource');
            displayResourceDetails(resource);
        });
    }

    // Display resource details
    function displayResourceDetails(resource) {
        var detailsContainer = $('#details-container');
        detailsContainer.empty();

        for (var key in resource) {
            if (resource.hasOwnProperty(key)) {
                var detail = $('<div class="resource-detail"></div>')
                    .text(key + ': ' + resource[key]);
                detailsContainer.append(detail);
            }
        }
    }

    populateResources();
    updateZoom();
});

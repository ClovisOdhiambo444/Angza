/**
 * Angza - AI Auditor
 * Frontend Application
 */

document.addEventListener('DOMContentLoaded', function() {
    // ============================================================
    // PAGE TRANSITIONS
    // ============================================================
    var pages = document.querySelectorAll('.page');
    var navBtns = document.querySelectorAll('.nav-link');
    var navHeight = 72;
    var isTransitioning = false;

    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function smoothScrollTo(targetY, duration) {
        duration = duration || 1000;
        return new Promise(function(resolve) {
            var startY = window.scrollY;
            var distance = targetY - startY;
            var startTime = performance.now();

            function step(currentTime) {
                var elapsed = currentTime - startTime;
                var progress = Math.min(elapsed / duration, 1);
                var eased = easeInOutCubic(progress);
                window.scrollTo(0, startY + distance * eased);
                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    resolve();
                }
            }
            requestAnimationFrame(step);
        });
    }

    function switchSection(targetId) {
        navBtns.forEach(function(btn) {
            btn.classList.remove('active');
            if (btn.getAttribute('data-section') === targetId) {
                btn.classList.add('active');
            }
        });
        pages.forEach(function(page) {
            page.classList.remove('active');
            if (page.id === targetId) {
                setTimeout(function() {
                    page.classList.add('active');
                }, 80);
            }
        });
    }

    navBtns.forEach(function(btn) {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            if (isTransitioning) return;
            isTransitioning = true;

            var targetId = this.getAttribute('data-section');
            var targetSection = document.getElementById(targetId);
            if (!targetSection) {
                isTransitioning = false;
                return;
            }

            switchSection(targetId);
            var targetRect = targetSection.getBoundingClientRect();
            var offsetTop = window.scrollY + targetRect.top - navHeight;
            await smoothScrollTo(offsetTop, 1000);

            setTimeout(function() {
                pages.forEach(function(page) {
                    if (page.id === targetId) {
                        page.classList.add('active');
                    } else {
                        page.classList.remove('active');
                    }
                });
                isTransitioning = false;
            }, 150);
        });
    });

    // Scroll Spy
    var observerOptions = {
        threshold: 0.4,
        rootMargin: '-' + navHeight + 'px 0px -10% 0px'
    };

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting && !isTransitioning) {
                var id = entry.target.id;
                navBtns.forEach(function(btn) {
                    btn.classList.remove('active');
                    if (btn.getAttribute('data-section') === id) {
                        btn.classList.add('active');
                    }
                });
                pages.forEach(function(page) {
                    page.classList.remove('active');
                    if (page.id === id) {
                        page.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    pages.forEach(function(page) {
        observer.observe(page);
    });
    switchSection('home');

    // ============================================================
    // FILE UPLOAD
    // ============================================================
    var fileInput = document.getElementById('fileInput');
    var uploadBtn = document.getElementById('uploadBtn');
    var loading = document.getElementById('loading');
    var resultsDiv = document.getElementById('results');
    var downloadSection = document.getElementById('downloadSection');

    if (uploadBtn) {
        uploadBtn.addEventListener('click', function() {
            fileInput.click();
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', async function(e) {
            var file = this.files[0];
            if (!file) return;

            uploadBtn.disabled = true;
            uploadBtn.innerHTML = '<span class="spinner"></span> Uploading...';
            loading.style.display = 'block';
            resultsDiv.classList.remove('visible');
            resultsDiv.innerHTML = '';
            if (downloadSection) downloadSection.classList.remove('visible');

            var formData = new FormData();
            formData.append('file', file);

            try {
                var response = await fetch('https://angza-backend.onrender.com/api/upload', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    var errorText = await response.text();
                    throw new Error('Server error (' + response.status + '): ' + errorText);
                }

                var data = await response.json();
                displayResults(data);

                if (downloadSection) downloadSection.classList.add('visible');

            } catch (error) {
                resultsDiv.innerHTML = '<div class="result-error">' +
                    '<strong>Error:</strong> ' + error.message +
                    '<p style="font-size:0.875rem;margin-top:0.5rem;color:#64748b;">' +
                    'Make sure the backend server is running at <code>https://angza-backend.onrender.com</code>.' +
                    '</p></div>';
                resultsDiv.classList.add('visible');
            } finally {
                uploadBtn.disabled = false;
                uploadBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Upload Document';
                loading.style.display = 'none';
                fileInput.value = '';
            }
        });
    }

    // ============================================================
    // DOWNLOAD HANDLERS
    // ============================================================
    function downloadReport(format) {
        var url = 'https://angza-backend.onrender.com/api/report/' + format;
        window.open(url, '_blank');
    }

    var downloadPdf = document.getElementById('downloadPdf');
    var downloadExcel = document.getElementById('downloadExcel');
    var downloadJson = document.getElementById('downloadJson');

    if (downloadPdf) {
        downloadPdf.addEventListener('click', function() {
            downloadReport('pdf');
        });
    }

    if (downloadExcel) {
        downloadExcel.addEventListener('click', function() {
            downloadReport('excel');
        });
    }

    if (downloadJson) {
        downloadJson.addEventListener('click', function() {
            downloadReport('json');
        });
    }

    // ============================================================
    // DISPLAY RESULTS
    // ============================================================
    function displayResults(data) {
        var risk = data.risk_score || 0;
        var riskClass = 'risk-low';
        if (risk > 70) riskClass = 'risk-high';
        else if (risk > 40) riskClass = 'risk-medium';

        var findingsHtml = '';
        if (data.findings && data.findings.length) {
            data.findings.forEach(function(f) {
                var severityClass = 'severity-low';
                if (f.severity > 70) severityClass = 'severity-high';
                else if (f.severity > 40) severityClass = 'severity-medium';

                findingsHtml += '<div class="finding-item">' +
                    '<div class="finding-clause">' + (f.clause || 'Clause') + '</div>' +
                    '<div class="finding-issue">' + (f.issue || '') + '</div>' +
                    '<div class="finding-recommendation"><strong>Recommendation:</strong> ' + (f.recommendation || '') + '</div>' +
                    '<div class="severity ' + severityClass + '">Severity: ' + f.severity + '/100</div>' +
                    '</div>';
            });
        } else {
            findingsHtml = '<p style="color:#64748b;">No specific findings identified.</p>';
        }

        var redFlagsHtml = '';
        if (data.red_flags && data.red_flags.length) {
            redFlagsHtml = data.red_flags.map(function(flag) {
                return '<div class="red-flag"><i class="fas fa-exclamation-triangle"></i> ' + flag + '</div>';
            }).join('');
        } else {
            redFlagsHtml = '<div class="red-flag" style="color:#059669;"><i class="fas fa-check-circle"></i> No critical red flags detected.</div>';
        }

        var keyTerms = data.key_terms || {};
        var keyTermsHtml = '<dl class="key-terms">';
        if (keyTerms.parties) keyTermsHtml += '<dt>Parties</dt><dd>' + keyTerms.parties + '</dd>';
        if (keyTerms.payment_terms) keyTermsHtml += '<dt>Payment Terms</dt><dd>' + keyTerms.payment_terms + '</dd>';
        if (keyTerms.termination) keyTermsHtml += '<dt>Termination</dt><dd>' + keyTerms.termination + '</dd>';
        if (keyTerms.liability_cap) keyTermsHtml += '<dt>Liability Cap</dt><dd>' + keyTerms.liability_cap + '</dd>';
        if (keyTerms.governing_law) keyTermsHtml += '<dt>Governing Law</dt><dd>' + keyTerms.governing_law + '</dd>';
        keyTermsHtml += '</dl>';

        resultsDiv.innerHTML =
            '<div class="result-header">' +
            '<h3>Audit Report</h3>' +
            '<span class="risk-score ' + riskClass + '">Risk Score: ' + risk + '/100</span>' +
            '</div>' +

            '<div class="result-section">' +
            '<h4>Key Terms</h4>' +
            keyTermsHtml +
            '</div>' +

            '<div class="result-section">' +
            '<h4>Findings</h4>' +
            findingsHtml +
            '</div>' +

            '<div class="result-section">' +
            '<h4>Red Flags</h4>' +
            redFlagsHtml +
            '</div>' +

            '<div class="result-footer">' +
            'Filename: ' + (data.filename || 'N/A') +
            '</div>';

        resultsDiv.classList.add('visible');
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});

from django.shortcuts import render

def index(request):
  data = {
    'windowLength': 0.02,
    'frameLength': 0.01,
    'mfccCoefficients': 13,
    'k': 1
  }
  
  if request.method == 'POST':
    data['windowLength'] = request.POST['windowLength']
    data['frameLength'] = request.POST['frameLength']
    data['mfccCoefficients'] = request.POST['mfccCoefficients']
    data['k'] = request.POST['k']

  return render(request, 'index.html', data)
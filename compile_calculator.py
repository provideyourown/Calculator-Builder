#!/usr/bin/env python

import sys
import re
import os


'''
Given text file defining the calculator form, compile it into wordpress plugin

length = 1 kg / ( 1240kgm^-3 * 3.14159265 * ( 0.003m / 2 )^2 )

density (text) = 1240
dia (select:{Diameter (mm), 1.4,3.0}) = 1.4
length (input:{Length(meters)}) = weight / ( density * 3.14159 * dia * dia * 0.25 ) )
weight (input:{Weight(gms)}) = length * density * 3.14159 * dia * dia * 0.25

density (select:{Density (gm/cm3), 1.25/PLA, 1.04/ABS}) = 1.25

'''

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def compileLine(line):
  code = line.split('//')[0].strip() # remove comments
  if not code:
    return None
  html = re.findall(r'"(.+)"', code)
  if html:
    return {'html': html[0]}
  parts = code.split('=')
  if not len(parts):
    return None
  left = parts[0]
  right = parts[1] if len(parts) > 1 else ''
  name = re.findall(r'\w+', left)[0]
  specs = re.findall(r'\((.*)\)', left)[0]
  pars = re.split(r'\:', specs)
  inType = pars[0]
  if len(pars) > 1:
    print 'pars: ' + str(pars)
    pars = re.findall(r'{(.*)}', pars[1])[0].split(',')
    label = pars[0]
    pars = pars[1:]
  else:
    label = name.capitalize()
    pars = []

  return {'name':name, 'type': inType, 'label': label, 'pars': pars, 'equation': right}




def generateFormDef(calc):
  name = calc['name']
  elemType = calc['type']
  label = calc['label']
  pars = calc['pars']
  equation = calc['equation']

  html = ''
  html += '<div class="form-field">'
  html += '<label for="%s">%s: </label>' % (name, label)

  if elemType == 'text':
    html += '<span id="%s">%s</span>' % (name, equation)
  elif elemType == 'input':
    html += '<input type="text" name="%s" value="" size="20" id="%s" />' % (name, name)
  elif elemType == 'select':
    html += '<select id="%s" name="%s" >' % (name, name)
    for par in pars:
      if '/' in par:
        parts = par.split('/')
        html += '<option value="%s">%s</option>' % (parts[0], parts[1])
      else:
        html += '<option value="%s">%s</option>' % (par, par)
    html += '</select>'
  else:
    pass # do nothing

  #html += '<img src="%s/img/question.png" alt="Help" title="%s" class="helpButton" style="cursor: pointer;">' % (iconDir, helpStr)
  #html += '<p class="error-msg">%s</p>' % errMsg

  #if not is_number(equation):
  #  html += '<a href="javascript:void(0)" id="calc_%s">Calculate</a>' % name
  html += '</div>'

  return html



def generateScriptCalc(calc, lines):
  name = calc['name']
  elemType = calc['type']
  #label = calc['label']
  #pars = calc['pars']
  equation = calc['equation']

  #if elemType == 'text':
  #  return None, None

  if is_number(equation):
    return None, None

  # its an equation - create the jscript function
  pars = [] # store up the pars for calculation on blur
  buf = ''
  funcName = 'calculate_%s' % name
  buf += '  function %s() {\n' % funcName
  #buf += '  $("%s#%s").change(function()\n' % (elemType, name)
  #buf += '  {\n'

  for line in lines:
    if 'name' in line: # skip html lines
      if line['name'] in equation: # only generate var if the parameter is in the equation
        if line['type'] == 'text':
          value = line['equation']
        else:
          value = 'parseFloat($("#%s").val())' % line['name']
        buf += '    var %s = %s;\n' % (line['name'], value)
      # append all pars for auto-calulation, because there may be dependencies on other fields
      pars.append(line['name'])
      #if (line['name'] != name) and not is_number(line['equation']):
      #  calculate = line['name']
      #  equation = line['equation']


  buf += '    var result = %s;\n' % equation
  if elemType == 'text':
    buf += '    $("#%s").html(result.toFixed(2));\n' % (name, )
  else:
    buf += '    $("#%s").val(result.toFixed(2));\n' % (name, )
  #buf += '    %s = %s;\n' % (calculate, equation)
  #buf += '  });\n'
  buf += '  }\n\n'

  #btn version - buf += '$("#calc_%s").click(calculate_%s);\n\n' % (name, name)
  #loose focus version:
  """for par in pars:
      if par != name:
          # calculate on change instead of blur - same as blur, but works on selects as well when changed
          buf += '  $("#%s").change(calculate_%s);\n' % (par, name)"""

  return funcName, buf


def generateAutoCalcFuncs(pars, funcs):
  # 1st generate the general refresh function to be called whenever a field changes
  # now generate the on change statements
  buf = ''
  for par in pars:
    buf += '  $("#%s").change(function () { \n' % par
    for func in funcs:
      if not par in func: # don't calculate the one being changed!
        buf += '%s(); \n' % func
    buf += '\n});\n\n'
  return buf





"**************************** Main Func ***********************************************"
# test module name == __main__; that way, we can import it into interpreter fdor testing
if __name__ == "__main__":


  args = sys.argv
  if len(args) != 2:
    print 'Invalid command format. Valid format:\n\ncompile_calculator.py <filename>.txt\n'
    exit()
  name = args[1]

  print 'Name: %s' % name

  baseName = './calculators/' + name
  fname = baseName + '.txt'
  if not os.path.exists(fname):
    print "File %s not found." % fname
    exit()
  with open(fname) as f:
      content = f.readlines()

  calcLines = []
  for line in content:
    #print "Line: %s" % line
    results = compileLine(line)
    if results:
      calcLines.append(results)

  htmlfile = open(baseName + '.html', 'w')  # clears the existing file
  for calc in calcLines:
    #print 'calc: ' + str(calc)
    if 'html' in calc:
      htmlfile.write(calc['html'] + '\n\n')
    else: 
      htmlfile.write(generateFormDef(calc) + '\n\n')

  # generate the js file
  scriptfile = open(baseName + '.js', 'w')  # clears the existing file
  scriptfile.write('jQuery(document).ready(function($) {\n')
  funcs = []
  # 1st - generate the general calculation functions
  for calc in calcLines:
    print 'calc' + str(calc)
    if not 'html' in calc:
      func, script = generateScriptCalc(calc, calcLines)
      if script:
        funcs.append(func)
        scriptfile.write(script + '\n\n')
  # 2nd - generate the auto-calculation on change lines
  pars = []
  for line in calcLines:
    if 'name' in line:
      pars.append(line['name'])
  script = generateAutoCalcFuncs(pars, funcs)
  scriptfile.write(script + '\n\n')
  scriptfile.write('});\n')



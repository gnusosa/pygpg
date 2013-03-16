""" pygpg - GnuPG python wrapper
    Copyright (C) 2012  https://www.abnorm.org/contact/

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from shlex import split
from subprocess import Popen,PIPE
from tempfile import mkstemp
from os import unlink

GPG_CMD='gpg'

def encrypt(txt,keys):
	if isinstance(keys,str):
		keys=(keys,)
	elif not isinstance(keys,tuple):
		try:
			keys=tuple(keys)
		except TypeError:
			return ''
	key_str='-R '+' -R '.join(keys)
	gpg=Popen(split('%s -q %s --batch --no-tty -a -o - -e -'%(GPG_CMD,key_str)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.write(txt)
	gpg.stdin.close()
	return gpg.stdout.read().strip()

def decrypt(txt):
	gpg=Popen(split('%s -q --batch --no-tty -o - -d -'%(GPG_CMD)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.write(txt)
	gpg.stdin.close()
	return gpg.stdout.read().strip()

def detach_sign(txt,key):
	gpg=Popen(split('%s -q -u %s --batch --no-tty -a -o - -b -'%(GPG_CMD,key)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.write(txt)
	gpg.stdin.close()
	return gpg.stdout.read().strip()

def clear_sign(txt,key):
	gpg=Popen(split('%s -q -u %s --batch --no-tty -a -o - --clearsign -'%(GPG_CMD,key)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.write(txt)
	gpg.stdin.close()
	return gpg.stdout.read().strip()

def sign(txt,key):
	gpg=Popen(split('%s -q -u %s --batch --no-tty -a -o - -s -'%(GPG_CMD,key)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.write(txt)
	gpg.stdin.close()
	return gpg.stdout.read().strip()

def verify(sign,signed_stream='',signed_file_name='',userid=''):
	if signed_file_name and signed_stream:
		return False
	if signed_stream:
		f,signed_file_name=mkstemp(prefix='pygpg-tmp-')
		f.write(signed_stream)
		f.close()
	gpg=Popen(split('%s -q --no-tty -a -o - --verify - %s'%(GPG_CMD,signed_file_name)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.write(sign)
	gpg.stdin.close()
	ret=gpg.wait()
	if signed_stream:
		unlink(signed_file_name)
	if ret==0:
		if userid:
			out=gpg.stdout.read()
			gpg.stdout.close()
			if out.find(userid)==-1:
				return False
		return True
	else:
		gpg.stdout.close()
		return False

def export_public_key(key):
	gpg=Popen(split('%s -q --batch --no-tty -a -o - --export %s'%(GPG_CMD,key)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.close()
	return gpg.stdout.read().strip()

def delete_key(fingerprint):
	gpg=Popen(split('%s -q --batch --no-tty -a -o - --delete-secret-and-public-key %s'%(GPG_CMD,fingerprint)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	ret=gpg.wait()
	if ret==0:
		return True
	else:
		return False

def import_public_key(key):
	gpg=Popen(split('%s -q --batch --no-tty -a -o - --import'%GPG_CMD), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stdin.write(key)
	gpg.stdin.close()
	ret=gpg.wait()
	if ret==0:
		return True
	else:
		return False

def import_public_from_server(key,server=''):
	if server:
		server=' --keyserver '+server
	gpg=Popen(split('%s -q --batch --no-tty -a -o - --recv-keys %s%s'%(GPG_CMD,key,server)), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	ret=gpg.wait()
	if ret==0:
		return True
	else:
		return False

def get_key_list():
	gpg=Popen(split('%s -q --batch --no-tty -a -o - -k --fingerprint'%GPG_CMD), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.close()
	output=gpg.stdout.read().strip()
	gpg.stdout.close()
	output=output.split('\n')[2:]
	res={}
	last=None
	for line in output:
		line=line.split()
		if len(line)==0:
			continue
		elif line[0]=='pub':
			last=line[1]
			res[line[1]]={}
		elif line[0]=='uid':
			if 'uids' in res[last]:
				res[last]['uids'].append(' '.join(line[1:]))
			else:
				res[last]['uids']=[' '.join(line[1:])]
		elif line[0]=='Key':
			res[last]['fingerprint']=' '.join(line[4:])
		elif line[0]=='sub':
			if 'subs' in res[last]:
				res[last]['subs'].append(line[1])
			else:
				res[last]['subs']=[line[1]]
	return res

def get_priv_key_list():
	gpg=Popen(split('%s -q --batch --no-tty -a -o - -K --fingerprint'%GPG_CMD), shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	gpg.stderr.close()
	gpg.stdin.close()
	output=gpg.stdout.read().strip()
	gpg.stdout.close()
	output=output.split('\n')[2:]
	res={}
	last=None
	for line in output:
		line=line.split()
		if len(line)==0:
			continue
		elif line[0]=='pub':
			last=line[1]
			res[line[1]]={}
		elif line[0]=='uid':
			if 'uids' in res[last]:
				res[last]['uids'].append(' '.join(line[1:]))
			else:
				res[last]['uids']=[' '.join(line[1:])]
		elif line[0]=='Key':
			res[last]['fingerprint']=' '.join(line[4:])
		elif line[0]=='sub':
			if 'subs' in res[last]:
				res[last]['subs'].append(line[1])
			else:
				res[last]['subs']=[line[1]]
	return res

from fabric.contrib.files import append, exists, sed, sudo
from fabric.api import local, run, env
import random

# for real
REPO_URL = 'git@github.com:bhandariroshan/mcqapp.git'
SITES_FOLDER = '/srv/www'
PROJECT_NAME = 'mcq'

HOST_FOLDER = "meroanswer"
DOMAIN_NAME = "meroanswer.com"
source_folder = '%s/%s/source' % (SITES_FOLDER, HOST_FOLDER)
STATIC_URL = '/static/'
push_type = "real"

code_only_folder = '%s/%s/source/%s' % (SITES_FOLDER, HOST_FOLDER, 'twitter_audit')

def prod():
    env.user = 'root'
    env.hosts = ['audeet.com']


def deploy():
    # _create_directory_structure_if_necessary(HOST_FOLDER)
    _get_latest_source(source_folder)
    _update_settings(source_folder)
    run('cd /srv/www/meroanswer/source/ && source ../virtualenv/bin/activate && python manage.py collectstatic')
    sudo ('reload %s'%(HOST_FOLDER))


  

def update_latest_code():
    settings_server_file = 'settings_server.py'
    if push_type == 'staging':
        settings_server_file = 'settings_staging_server.py'
    run('cd %s && git reset --hard && git clean -f -d && git checkout master && git pull && git pull origin master' % (source_folder))
    _update_virtualenv(source_folder)
    settings_path = source_folder + '/' + PROJECT_NAME + '/settings.py'
    settings_server_path = source_folder + '/' + PROJECT_NAME + '/' + settings_server_file
    run("touch %s" % (settings_path))
    run("rm %s" % (settings_path))
    run('cp %s %s' % (settings_server_path, settings_path))
    # run ("cd %s && python manage.py collectstatic"%(source_folder))
    _update_static_files(source_folder)
    _update_database(source_folder)
    # _run_gunicorn()
    sudo("service nginx reload")
    sudo("service nginx restart")
    sudo("reload %s" % (HOST_FOLDER))


def reboot():
    sudo("reboot")


def _create_directory_structure_if_necessary(site_name):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s/%s' % (SITES_FOLDER, site_name, subfolder)) 

def _get_latest_source(source_folder):
    # run('cd %s && git reset --hard && git clean -f -d && git checkout master && git pull -f' % (source_folder))
    

    if exists(source_folder + '/.git'): #1
        run('cd %s && git fetch && git pull && git checkout master' % (source_folder,)) #23
    else:
        run('git clone %s %s' % (REPO_URL, source_folder)) #4
    current_commit = local("git log -n 1 --format=%H", capture=True) #5
    # run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder):
    settings_path = source_folder + '/' + PROJECT_NAME + '/settings.py'
    settings_server_path = source_folder + '/' + PROJECT_NAME + '/' + 'settings_remote.py'
    run("touch %s" % (settings_path))
    run("rm %s" % (settings_path))
    run('cp %s %s' % (settings_server_path, settings_path))
    

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'): #1
        run('virtualenv --python=python2.7 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirement.txt' % ( #2
            virtualenv_folder, source_folder
    ))

    run('source %s/bin/activate' % (virtualenv_folder))

def _update_static_files(code_only_folder):
    # sed('%s/%s/source/%s' % (SITES_FOLDER, HOST_FOLDER, 'twitter_audit/manage.py'), "settings.local", 'settings.production', use_sudo=True) #1

    virtualenv_folder = source_folder + '/../virtualenv'
    run('source %s/bin/activate' % (virtualenv_folder))

    run('cd %s && python manage.py  collectstatic --noinput' % ( # 1
        '%s/%s/source/' % (SITES_FOLDER, HOST_FOLDER)
    ))

# def _update_database(source_folder):
#     run('cd %s && ../virtualenv/bin/python3 manage.py syncdb --noinput' % (
#         source_folder,
#     ))

def _update_database(source_folder):
    
    # first_time = False
    # if first_time == True:
    #     run('cd %s && ../virtualenv/bin/python2.7 manage.py syncdb' % (source_folder,))
    #     # one-off fake database migration. remove me before next deploy
    #     run('cd %s && ../virtualenv/bin/python2.7 manage.py migrate lists --fake 0001' % (
    #         source_folder,
    #     ))
    #     run('cd %s && ../virtualenv/bin/python2.7 manage.py migrate' % (source_folder,))
    # else:
    #     run('cd %s && ../virtualenv/bin/python2.7 manage.py syncdb --migrate --noinput' % (
    #         source_folder,
    #     ))
    run('cd %s && python manage.py syncdb' % ('%s/%s/source/' % (SITES_FOLDER, HOST_FOLDER)))


### automating all other processes like nginx
def initial_server_deployment():
    # _install_package_from_apt()
    # _create_directory_structure_if_necessary(HOST_FOLDER)
    # _get_latest_source(source_folder)
    # _update_settings(source_folder, HOST_FOLDER)
    # _update_virtualenv(source_folder)
    # _update_static_files(source_folder)
    # _update_database(source_folder)
    # _run_nginx()
    _run_upstart()


def _install_package_from_apt():
    sudo('apt-get install git')
    sudo('apt-get install python-pip')
    sudo('pip install virtualenv')
    sudo('apt-get install nginx')
    sudo('apt-get install python-dev')

def _run_gunicorn():
    run('cd %s &&../virtualenv/bin/gunicorn --bind unix:/tmp/%s.socket %s.wsgi:application --access-logfile %s/%s --log-file %s/%s'%( source_folder,
             DOMAIN_NAME, PROJECT_NAME, VIRTUAL_FOLDER, 'guincorn-access.log',  VIRTUAL_FOLDER, 'guinicorn-error_logs.log'))

def _run_nginx():
   
    sites_available = '/etc/nginx/sites-available/%s' % (HOST_FOLDER)
    sites_enabled = '/etc/nginx/sites-enabled/%s' % (HOST_FOLDER)
    sudo('cp %s/deploy_tools/nginx.template.conf %s'%(source_folder, sites_available))
    sed(sites_available, "SITENAME", DOMAIN_NAME, use_sudo=True) #1
    sed(sites_available, "SITES_FOLDER", SITES_FOLDER, use_sudo=True) #1
    sed(sites_available, "HOST_FOLDER", HOST_FOLDER, use_sudo=True) #1
    sudo("rm %s.bak"%(sites_available))
    
    sudo("ln -s %s %s"%(sites_available, sites_enabled))
    run('mkdir -p %s/%s/logs'%(SITES_FOLDER,HOST_FOLDER)) 
    run('cd %s/%s && touch nginx-access.log'%(SITES_FOLDER,HOST_FOLDER))
    run('cd %s/%s && touch nginx-error.log'%(SITES_FOLDER,HOST_FOLDER))
    sudo('service nginx reload')
    sudo('service nginx restart')

def _run_upstart():
    upstart_file = "/etc/init/%s.conf" %(HOST_FOLDER)
    sudo('cp %s/deploy_tools/gunicon-upstart.template.conf %s'%(source_folder, upstart_file))
    
    sed(upstart_file, "SITENAME", HOST_FOLDER, use_sudo=True) #1
    sed(upstart_file, "SITES_FOLDER", SITES_FOLDER, use_sudo=True) #1
    sed(upstart_file, "PROJECT_NAME", PROJECT_NAME, use_sudo=True) #1
    sed(upstart_file, "DOMAIN_NAME", DOMAIN_NAME, use_sudo=True) #1
    sudo('rm %s.bak'%(upstart_file))
    # sudo("sed -i 's/SITENAME/%s/g' /etc/init/%s.conf" % (HOST_FOLDER, HOST_FOLDER))
    # sudo("sed -i 's/SITES_FOLDER/%s/g' /etc/init/%s.conf" % (SITES_FOLDER, HOST_FOLDER))
    # sudo("sed -i 's/PROJECT_NAME/%s/g' /etc/init/%s.conf" % (PROJECT_NAME, HOST_FOLDER))
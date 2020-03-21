#
# Conditional build:
%bcond_without	doc	# ri/rdoc documentation

%define pkgname thread_order
Summary:	Test helper for ordering threaded code
Summary(pl.UTF-8):	Funkcje pomocnicze dla testów do ustalania porządku kodu w wątkach
Name:		ruby-%{pkgname}
Version:	1.1.0
Release:	2
License:	MIT
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	80b8b69edb211e97e30dc7334e37a593
Group:		Development/Languages
URL:		https://github.com/JoshCheek/thread_order
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Test helper for ordering threaded code (does not depend on gems
or stdlib, tested on 1.8.7 - 2.2, rbx, jruby).

%description -l pl.UTF-8
Funkcje pomocnicze dla testów do ustalania porządku kodu w wątkach
(niezależnie od gemów ani biblioteki standardowej, przetestowany na
implementacjach 1.8.7 - 2.2, rbx, jruby).

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

#'

%if %{with doc}
rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} ri/created.rid
%{__rm} ri/cache.ri
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License.txt Readme.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/ThreadOrder
%endif
